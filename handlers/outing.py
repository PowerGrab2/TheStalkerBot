'''Отправиться на вылазку'''

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from create_bot import bot, dp
from states.stateGuns import FSMOuting, FSMMainMenu, outingForest, outingitems
from keyboards.client_kb import ikb_outing, ikb_outing_ac, ikb_outing_anonimous, kb_main_menu, ikb_next, ikb_outing_fight_stat1, ikb_outing_fight_stat2, ikb_return_to_main_menu
from items.location_items import *
from items.guns_items import *
from items.enemys_items import *
from items.items_items import *
from data_base.sqlite_db import current_exp, current_energy, minus_energy, minus_credit_balance, plus_credit_balance, \
    current_gun, get_credit_balance, get_count_item, minus_count_item, plus_exp
import random
import asyncio
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup




# @dp.callback_query_handler(text='outing', state=FSMOuting.wait_answer)
async def outing_menu(callback: types.CallbackQuery, state: FSMContext):
    '''Менюшка выбора категории'''
    await FSMOuting.wait_answer.set()
    async with state.proxy() as data:
        data['wait_answer'] = callback.message.message_id

        await callback.message.edit_text(text='Выбирите тип вылазки:',
                                         reply_markup=ikb_outing)

        await FSMOuting.next()

# dp.callback_query_handler(text='active_outing', state=FSMOuting.pick_outing_category)
async def outing_locations(callback: types.CallbackQuery, state: FSMContext):
    '''Получаем калбек с категорией'''
    async with state.proxy() as data:
        if callback.message.message_id != data['wait_answer']:
            await callback.answer(text='Сессия проходит вдругом меню', show_alert=True)
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            return

        elif callback.data == 'active_outing':
            await callback.message.edit_text(text='Куда отправимся?\n'
                                                  '\n'
                                                  f"<b>Локация №1:</b> <em>{location_forest['name']}</em>\n"
                                                  f"<b>Сложность:</b> <em>{location_forest['difficult']}</em>\n"
                                                  f"<b>Награда за вылазку:</b> <em>{location_forest['money'][0]} - {location_forest['money'][1]} CR</em>\n"
                                                  f"<b>Требуеться енергии:</b> <em>{location_forest['energy']} ед.</em>\n"
                                                  f"<b>Требуемый опыт:</b> <em>{location_forest['exp']} ед.</em>\n"
                                                  f"\n"
                                                  f"<i>Выберите локацию</i>",
                                             parse_mode='html',
                                             reply_markup=ikb_outing_ac)
            await FSMOuting.next()

        elif callback.data == 'passive_outing':
            await out
            return

        elif callback.data == 'main_menu':
            if callback.message.message_id != data['wait_answer']:
                await callback.answer(text='Сессия проходит в другом меню', show_alert=True)
                await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
                return

            await state.finish()
            await callback.message.edit_text(text="Добро пожаловать, сталкер\n"
                                                  f"Рад тебя снова видеть, чем займешься?\n"
                                                  f"/start",
                                             reply_markup=kb_main_menu)
            await FSMMainMenu.wait_message.set()
            data['*'] = callback.message.message_id

# @dp.callback_query_handler(state=FSMOuting.pick_location)
async def pick_current_location(callback: types.CallbackQuery, state: FSMContext):
    '''Получаем калбек текущей локации'''
    user_id = callback.from_user.id
    async with state.proxy() as data:
        if callback.message.message_id != data['wait_answer']:
            await callback.answer(text='Сессия проходит вдругом меню', show_alert=True)
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            return

        elif callback.data == 'forest':
            if int(await current_exp(user_id)) >= 0:
                if int(await current_energy(user_id)) > 0:
                    # Енергия
                    await minus_energy(callback.from_user.id, 1)
                    await callback.answer(text='Енергия -1')
                    # Локация
                    
                    await outingForest.stat_set.set()
                    await stats_set(callback, state)


        elif callback.data == 'back':
            await outing_menu(callback, state)

# @dp.callback_query_handler(state=outingForest.stat_set)
async def stats_set(callback: types.CallbackQuery, state=FSMContext):
    async with state.proxy() as data:
        if callback.message.message_id != data['wait_answer']:
            await callback.answer(text='Сессия проходит вдругом меню', show_alert=True)
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            return
        

        # Характеристики
        if callback.data == 'forest':
            cur_loc = location_forest
        data['location'] = cur_loc
        data['pick_outing_category'] = data['location']['console_name']
        data['health'] = 100
        data['max_health'] = data['health']
        random_events = ['anonimous']
        data['random_event'] = random.choice(random_events)  # Событие
        data['time'] = 1.5
        data['fight'] = '2x'
        data['win_money'] = random.randint(location_forest['money'][0], location_forest['money'][1])
        data['money'] = 0
        data['exp'] = random.randint(data['location']['plus_exp'][0], data['location']['plus_exp'][1])
        data['mini_boss'] = True
        data['boss'] = True
        data['win'] = False
        if data['random_event'] == 'anonimous':
            await callback.message.edit_text(
                text='<i>Вы решили отправиться в Лес, по дороге вы увидели незнакомца <b>который идет в вашу сторону</b></i>',
                parse_mode='html')
            await asyncio.sleep(2.5)
            await callback.message.edit_reply_markup(reply_markup=ikb_outing_anonimous)
            await outingForest.next()


# dp.callback_query_handler(state=outingForest.get_answer)
async def get_ivent_answer(callback: types.CallbackQuery, state: FSMContext):
    '''Получаем ответ со случайного события'''

    async with state.proxy() as data:
        if callback.message.message_id != data['wait_answer']:
            await callback.answer(text='Сессия проходит вдругом меню', show_alert=True)
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            return

        elif data['pick_outing_category'] == 'forest':
            if data['random_event'] == 'anonimous':
                
                
                if callback.data == 'yes':
                    if random.randint(0, 2) and int((await get_credit_balance(callback.from_user.id))) > 19:
                        money = random.randint(20, 41)
                        await minus_credit_balance(callback.from_user.id, money)
                        await callback.message.edit_text(text=f'<i>Незнакомец прошел мимо вас, проверив карманы вы поняли, что <b>у вас пропали {money} CR</b>, немного расстроившись вы пошли дальше</i>',
                                                         parse_mode='html')
                        await callback.answer(text=f"Списано {money} CR")
                        await asyncio.sleep(2.5)
                        await callback.message.edit_reply_markup(ikb_next)
                        await outingForest.next()
                    else:
                        await callback.message.edit_text(text='<i>Незкомецем оказался ваш друг - Николай, после минутки болтовни вы пошли дальше</i>',
                                                         parse_mode='html')
                        await asyncio.sleep(2.5)
                        await callback.message.edit_reply_markup(ikb_next)
                        await outingForest.next()
                        
                        
                elif callback.data == 'no':
                    if random.randint(0, 2) and int((await get_credit_balance(callback.from_user.id))) > 19:
                        money = random.randint(20, 41)
                        await minus_credit_balance(callback.from_user.id, money)
                        await callback.message.edit_text(text=f'<i>Свернув с тропинки вы обошли незнакомца, но вскорее вы поняли, что где-то потеряли {money} CR. Обидно, но что поделать, вы отправились дальше</i>',
                                                         parse_mode='html')
                        await callback.answer(text=f"Списано {money} CR")
                        await asyncio.sleep(2.5)
                        await callback.message.edit_reply_markup(ikb_next)
                        await outingForest.next()
                    else:
                        await callback.message.edit_text(text='<i>Вы решили обойти незнакомца, может и не зря... Так или иначе вы продолжили свой путь к лагерю</i>',
                                                         parse_mode='html')
                        await asyncio.sleep(2.5)
                        await callback.message.edit_reply_markup(ikb_next)
                        await outingForest.next()

async def continue_story1(callback: types.CallbackQuery, state: FSMContext):

    async with state.proxy() as data:
        if callback.message.message_id != data['wait_answer']:
            await callback.answer(text='Сессия проходит вдругом меню', show_alert=True)
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            return

        elif data['pick_outing_category'] == 'forest':
            if callback.data == 'next':
                data['enemy'] = radiation_wolf
                data['max_enemy_health'] = data['enemy']['health']
                await callback.message.edit_text(text=f"<i>Приближившись к лагерю <b>вы кого то замечаете...</b>\n"
                                                      f"Оно крайне похоже на зараженного волка, который жаждит вкусно поесть</i>",
                                                 parse_mode='html')
                await asyncio.sleep(3.3)
                await callback.message.edit_reply_markup(ikb_next)
                await outingForest.next()

async def continue_story2(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if callback.message.message_id != data['wait_answer']:
            await callback.answer(text='Сессия проходит вдругом меню', show_alert=True)
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            return

        elif data['pick_outing_category'] == 'forest':
            if callback.data == 'next':
                await callback.message.edit_text(
                    text=f"<i>Вы попытались тихо уйти, но наступили на сухую ветку, тем самым "
                         f"вы привлекли внимание волка, <b>драки не избежать</b></i>",
                    parse_mode='html')
                await asyncio.sleep(3)
                await callback.message.edit_reply_markup(ikb_next)
                await outingForest.next()


async def outing_fight_mn(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if callback.message.message_id != data['wait_answer']:
            await callback.answer(text='Сессия проходит вдругом меню', show_alert=True)
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            return

        if callback.data == 'next':
            await FSMOuting.stat_fight.set()
            await outing_fight_stats(callback, state)

async def outing_fight_stats(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if callback.message.message_id != data['wait_answer']:
            await callback.answer(text='Сессия проходит вдругом меню', show_alert=True)
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            return






        await callback.message.edit_text(text=f"<i>Характеристика боя:\n"
                                              f"Здоровье {callback.from_user.first_name}: <b>{data['health']} хп</b>\n"
                                              f"\n"
                                              f"Здоровье {data['enemy']['name']}: <b>{data['enemy']['health']} хп</b></i>",
                                         reply_markup=ikb_outing_fight_stat1(data['fight']),
                                         parse_mode='html')

        await FSMOuting.next()





async def outing_fight(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if callback.message.message_id != data['wait_answer']:
            await callback.answer(text='Сессия проходит вдругом меню', show_alert=True)
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            return


        async def random_damage(bool: int) -> int:
            '''Получить рандомный дамаг. 1 - Игрок, 0 - Враг'''
            if bool:
                return random.randint((await current_gun(callback.from_user.id))['damage'][0],
                                      (await current_gun(callback.from_user.id))['damage'][1])
            else:
                return random.randint(data['enemy']['damage'][0], data['enemy']['damage'][1])

        if callback.data == 'speed':
            print(data['time'])
            if data['time'] == 3:
                data['time'] = 1.5
                data['fight'] = '2x'
                await callback.message.edit_reply_markup(reply_markup=ikb_outing_fight_stat1(data['fight']))
                return

            else:
                data['time'] = 3
                data['fight'] = '1x'
                await callback.message.edit_reply_markup(reply_markup=ikb_outing_fight_stat1(data['fight']))
                return




        elif callback.data == 'atack':
            print(data['health'])
            my_atack_phrase = ['Взяв оружие вы нанесли повторный удар', f"Вы выстрелели в {data['enemy']['name']}"]
            my_atack_phrase_crit = ['Выдыхнув вы нацелились волку в голову, выстрельнув, вы попали ему в глаз нанеся']
            my_atack_phrase_lose = ['Вы не в состоянии атаковать', 'Оружие заклинило, вы не сможете проатаковать']

            medmg = await random_damage(1) # Мой дамаг
            hedmg = await random_damage(0) # Дамаг Врага

            if random.randint(1, 5) != 1:

                # Моя атака
                await callback.message.edit_text(text=f"<i>{random.choice(my_atack_phrase)}, тем самым нанеся <b>{medmg} очков урона</b></i>",
                                                 parse_mode='html')
                data['enemy']['health'] -= medmg
                await asyncio.sleep(data['time'])

            else:

                if random.randint(0, 2):

                    # Моя крит атака
                    await callback.message.edit_text(
                        text=f"<b>{random.choice(my_atack_phrase_crit)} {(await current_gun(user_id=callback.from_user.id))['damage'][2]} очков урона</b>",
                    parse_mode='html')
                    data['enemy']['health'] -= (await current_gun(callback.from_user.id))['damage'][2]
                    await asyncio.sleep(3)

                else:

                    # Мой провальный удар
                    await callback.message.edit_text(
                        text=f"<b>{random.choice(my_atack_phrase_lose)}</b>",
                        parse_mode='html')
                    await asyncio.sleep(3)



            if random.randint(1, 5) != 1:

                # Атака врага
                await callback.message.edit_text(text=f"<i>{data['enemy']['name']} {random.choice(data['enemy']['atack_phrase'])}, вы потеряли <b>{hedmg} хп</b></i>",
                                                 parse_mode='html')
                data['health'] -= hedmg
                await asyncio.sleep(data['time'])


            else:

                if random.randint(0, 2):

                    # Крит атака врага
                    await callback.message.edit_text(
                        text=f"<b>{data['enemy']['name']} {random.choice(data['enemy']['atack_phrase_crit'])} {data['enemy']['damage'][2]} очков хп</b>",
                        parse_mode='html')
                    data['health'] -= data['enemy']['damage'][2]
                    await asyncio.sleep(4)

                else:

                    # Провальная атака врага
                    await callback.message.edit_text(
                        text=f"<b>{data['enemy']['name']} {random.choice(data['enemy']['atack_phrase_lose'])}</b>",
                        parse_mode='html')
                    await asyncio.sleep(3)


            if data['enemy']['health'] > 0:
                if data['health'] > 0:

                    await callback.message.edit_text(text=f"<i>Характеристика боя:\n"
                                              f"Здоровье {callback.from_user.first_name}: <b>{data['health']} хп</b>\n"
                                              f"\n"
                                              f"Здоровье {data['enemy']['name_s']}: <b>{data['enemy']['health']} хп</b></i>",
                                         reply_markup=ikb_outing_fight_stat1(data['fight']),
                                         parse_mode='html')
                    return

            else:
                
                if data['boss']:
                    last_enemy = data['enemy']['name_s']
                    data['enemy'] = blood_eater
                    data['max_enemy_health'] = data['enemy']['health']
                    await callback.message.edit_text(text=f"Вы одержали победу над {last_enemy}, после чего собрали ценный лут и решили отправиться домой, но по дороге назад встретили {data['enemy']['name_s']}")
                    await asyncio.sleep(2.5)
                    await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Начать бой', callback_data='next')))
                    data['boss'] = False
    
                    await FSMOuting.stat_fight.set()
                else:
                    await callback.message.edit_text(text=f"<i>{data['enemy']['name_s']} побежден, вы незамедлительно продолжили путь и дошли в мирную зону</i>",
                                                     parse_mode='html')
                    await asyncio.sleep(2.5)
                    await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Закончить вылазку', callback_data='next')))
                    data['win'] = True
                    await FSMOuting.end_screen.set()
                    











        elif callback.data == 'item':




            ikb_outing_items_med = InlineKeyboardButton(text=f"Аптечка 💊 {await get_count_item(user_id=callback.from_user.id, item='med')}|5", callback_data='med')
            ikb_outing_items_grenade = InlineKeyboardButton(text=f"Граната 💣 {await get_count_item(user_id=callback.from_user.id, item='grenade')}|5", callback_data='grenade')
            ikb_outing_items_back = InlineKeyboardButton(text=f"Вернуться назад ◀️", callback_data='back')

            ikb_outing_items = InlineKeyboardMarkup(row_width=2).add(ikb_outing_items_med, ikb_outing_items_grenade).add(ikb_outing_items_back)

            await callback.message.edit_text(text='Данные о предметах:\n'
                                                  f"{med['name']} - востанавливает 25% хп\n"
                                                  f"{grenade['name']} - наносит 20% урона врагу, при этом оглушая его на 1 ход\n"
                                                  f"\n"
                                                  f"Выбирите доступный предмет: ",
                                             reply_markup=ikb_outing_items)
            await outingitems.get_item.set()


async def outing_items(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if callback.message.message_id != data['wait_answer']:
            await callback.answer(text='Сессия проходит вдругом меню', show_alert=True)
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            return

        if callback.data == 'med':
            if (await get_count_item(callback.from_user.id, item='med')) > 0:
                if data['health'] == data['max_health']:
                    await FSMOuting.fight.set()
                    await callback.answer(text=f"У вас максимальное хп")
                    await callback.message.edit_text(text=f"<i>Характеристика боя:\n"
                                                          f"Здоровье {callback.from_user.first_name}: <b>{data['health']} хп</b>\n"
                                                          f"\n"
                                                          f"Здоровье {data['enemy']['name']}: <b>{data['enemy']['health']} хп</b></i>",
                                                     reply_markup=ikb_outing_fight_stat1(data['fight']),
                                                     parse_mode='html')
                    return



                elif data['health'] + int((data['max_health'] * med['add_hp'])) <= data['max_health']:
                    await minus_count_item(callback.from_user.id, item='med')
                    data['health'] += int((data['max_health'] * med['add_hp']))
                    await FSMOuting.fight.set()
                    await callback.answer(text=f"Вы использовали аптечку")
                    await callback.message.edit_text(text=f"<i>Характеристика боя:\n"
                                              f"Здоровье {callback.from_user.first_name}: <b>{data['health']} хп</b>\n"
                                              f"\n" 
                                              f"Здоровье {data['enemy']['name']}: <b>{data['enemy']['health']} хп</b></i>",
                                         reply_markup=ikb_outing_fight_stat1(data['fight']),
                                         parse_mode='html')
                    return
                else:
                    data['health'] = data['max_health']
                    await minus_count_item(callback.from_user.id, item='med')
                    await FSMOuting.fight.set()
                    await callback.answer(text=f"Вы использовали аптечку")
                    await callback.message.edit_text(text=f"<i>Характеристика боя:\n"
                                                          f"Здоровье {callback.from_user.first_name}: <b>{data['health']} хп</b>\n"
                                                          f"\n"
                                                          f"Здоровье {data['enemy']['name']}: <b>{data['enemy']['health']} хп</b></i>",
                                                     reply_markup=ikb_outing_fight_stat1(data['fight']),
                                                     parse_mode='html')
                    return
            else:
                await callback.answer(text=f"У вас нету аптечек")
                return

        elif callback.data == 'grenade':
            if (await get_count_item(callback.from_user.id, item='grenade')) > 0:
                await minus_count_item(user_id=callback.from_user.id, item='grenade')
                await callback.message.edit_text(text=f"<i>Вы кинули гранату прямо в цель, нанеся <b>{int(data['max_enemy_health'] * grenade['damage'])} очков урона</b>, при этом оглушив ее</i>",
                                                 parse_mode='html')
                data['enemy']['health'] -= int(data['max_enemy_health'] * grenade['damage'])
                await asyncio.sleep(3)
                if data['enemy']['health'] <= 0:
                    last_enemy = data['enemy']['name']
                    data['enemy'] = blood_eater
                    data['max_enemy_health'] = data['enemy']['health']
                    await callback.message.edit_text(f"<b>ВЫ ВЗОРВАЛИ {data['enemy']['name']}, вы победили !</b>",
                                                     parse_mode='html')
                    await asyncio.sleep(2.5)
                    await callback.message.edit_reply_markup(reply_markup=ikb_next)

                    await FSMOuting.stat_fight.set()
                else:
                    await FSMOuting.fight.set()
                    await callback.answer(text=f"Вы использовали гранату")
                    await callback.message.edit_text(text=f"<i>Характеристика боя:\n"
                                                          f"Здоровье {callback.from_user.first_name}: <b>{data['health']} хп</b>\n"
                                                          f"\n"
                                                          f"Здоровье {data['enemy']['name']}: <b>{data['enemy']['health']} хп</b></i>",
                                                     reply_markup=ikb_outing_fight_stat1(data['fight']),
                                                     parse_mode='html')
                    return
            else:
                await callback.answer(text='У вас нету гранат')
                return

        elif callback.data == 'back':
            await FSMOuting.fight.set()
            await callback.message.edit_text(text=f"<i>Характеристика боя:\n"
                                                  f"Здоровье {callback.from_user.first_name}: <b>{data['health']} хп</b>\n"
                                                  f"\n"
                                                  f"Здоровье {data['enemy']['name']}: <b>{data['enemy']['health']} хп</b></i>",
                                             reply_markup=ikb_outing_fight_stat1(data['fight']),
                                             parse_mode='html')
            return



async def outing_end_screen(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if callback.message.message_id != data['wait_answer']:
            await callback.answer(text='Сессия проходит вдругом меню', show_alert=True)
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            return
        
        
        if callback.data == 'next':
            if data['win']:
                data['money'] += data['win_money']
            else:
                data['money'] += data['location']['lose_money']
            
            await plus_credit_balance(callback.from_user.id, data['money'])
            await plus_exp(callback.from_user.id, data['exp'])
            
            await callback.answer('Вы закончили вылазку')
            await callback.message.edit_text(text=f"Итоги вылазки:\n"
                                             f"\n"
                                             f"Всего заработано CR: {data['money']}\n"
                                             f"Опыта получено: {data['exp']}",
                                             reply_markup=ikb_return_to_main_menu)
            await FSMOuting.next()

async def outing_return_to_mn(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if callback.message.message_id != data['wait_answer']:
            await callback.answer(text='Сессия проходит вдругом меню', show_alert=True)
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            return
        
        data['*'] = callback.message.message_id

        await state.finish()

        await callback.message.edit_text(text="Добро пожаловать, сталкер\n"
                                              f"Рад тебя снова видеть, чем займешься?\n"
                                              f"/start",
                                         reply_markup=kb_main_menu)
        await FSMMainMenu.wait_message.set()
    
    







def register_outing_handlers(dp: Dispatcher):
    # Меню
    dp.register_callback_query_handler(outing_menu, text='outing', state=FSMOuting.wait_answer)
    dp.register_callback_query_handler(outing_locations, state=FSMOuting.pick_outing_category)
    dp.register_callback_query_handler(pick_current_location, state=FSMOuting.pick_location)
    # Зараженный лес
    dp.register_callback_query_handler(stats_set, state=outingForest.stat_set)
    dp.register_callback_query_handler(get_ivent_answer, state=outingForest.get_answer)
    dp.register_callback_query_handler(continue_story1, state=outingForest.get_continue1)
    dp.register_callback_query_handler(continue_story2, state=outingForest.get_continue2)
    dp.register_callback_query_handler(outing_fight_mn, state=outingForest.fight_mn)
    dp.register_callback_query_handler(outing_fight_stats, state=FSMOuting.stat_fight)
    dp.register_callback_query_handler(outing_fight, state=FSMOuting.fight)
    dp.register_callback_query_handler(outing_items, state=outingitems.get_item)
    dp.register_callback_query_handler(outing_end_screen, state=FSMOuting.end_screen)
    dp.register_callback_query_handler(outing_return_to_mn, state=FSMOuting.return_to_mn)





