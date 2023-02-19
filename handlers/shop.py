'''Торговая лавка'''
from aiogram import types, Dispatcher
from create_bot import dp, bot
from data_base.sqlite_db import buy_gun, have_gun, get_credit_balance, minus_credit_balance
from aiogram.dispatcher import FSMContext
from states.stateGuns import FSMShop, FSMMainMenu
from items.guns_items import *
from keyboards.client_kb import ikb_shop, ikb_shop_guns_pick, ikb_shop_pick, ikb_return_to_main_menu, kb_main_menu
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



#@dp.callback_query_handler(text='shop', state=FSMShop.examination_guns)
async def shop_menu(callback: types.CallbackQuery, state: FSMContext):
    '''Менюшка выбора категорий магазина'''
    await FSMShop.examination_guns.set()
    async with state.proxy() as data:

        # Айди текущего сообщения
        data['pick_shop_category'] = callback.message.message_id

        await callback.message.edit_text(text=f"Привет сталкер, тебе чего?",
                                         reply_markup=ikb_shop)

        await FSMShop.next()

async def gun_shop_examination(callback: types.CallbackQuery, state: FSMContext):
    '''Проверка на наличие оружия'''
    async with state.proxy() as data:
        if callback.message.message_id != data['pick_shop_category']:
            await callback.answer(text='Сессия проходит вдругом меню', show_alert=True)
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            return

        elif callback.data == 'gun_shop':
            guns_shop = []
            async with state.proxy() as data:
                data['examination_guns'] = False
                # Проверка 'Есть ли инное оружие' ! True - добавить в инвентарь !
                if not data['examination_guns']:
                    if not await have_gun(callback.from_user.id, pistol_pmm['console_name']):
                        guns_shop.append(pistol_pmm['name'])
                    if not await have_gun(callback.from_user.id, pistol_marta['console_name']):
                        guns_shop.append(pistol_marta['name'])
                    if not await have_gun(callback.from_user.id, drobovik_obrez['console_name']):
                        guns_shop.append(drobovik_obrez['name'])

                    # Пистолет Пмм
                    if pistol_pmm['name'] in guns_shop:
                        pistol_pmm_1 = f"<b>1 - {pistol_pmm['name']}</b> - наносит от {pistol_pmm['damage'][0]} до {pistol_pmm['damage'][1]} очков урона\n" \
                                       f"Цена: {pistol_pmm['price']} CR\n" \
                                       f"{'-' * 50}"
                        ikb_shop_guns_pick_1 = InlineKeyboardButton(text=f'1 ✅', callback_data=1)
                        pistol_pmm_examination = True
                    else:
                        pistol_pmm_1 = f"<b>1 - {pistol_pmm['name']}</b> - наносит от {pistol_pmm['damage'][0]} до {pistol_pmm['damage'][1]} очков урона\n" \
                                       f"Распродано\n" \
                                       f"{'-' * 50}"
                        ikb_shop_guns_pick_1 = InlineKeyboardButton(text=f'1 ❎', callback_data=1)
                        pistol_pmm_examination = False

                    # Пистолет Марта
                    if pistol_marta['name'] in guns_shop:
                        pistol_marta_2 = f"<b>2 - {pistol_marta['name']}</b> - наносит от {pistol_marta['damage'][0]} до {pistol_marta['damage'][1]} очков урона\n" \
                                         f"Цена: {pistol_marta['price']} CR\n" \
                                         f"{'-' * 50}"
                        ikb_shop_guns_pick_2 = InlineKeyboardButton(text=f'2 ✅', callback_data=2)
                        pistol_marta_examination = True
                    else:
                        pistol_marta_2 = f"<b>2 - {pistol_marta['name']}</b> - наносит от {pistol_marta['damage'][0]} до {pistol_marta['damage'][1]} очков урона\n" \
                                         f"Распродано\n" \
                                         f"{'-' * 50}"
                        ikb_shop_guns_pick_2 = InlineKeyboardButton(text=f'2 ❎', callback_data=2)
                        pistol_marta_examination = False

                    # Дробовик обрез
                    if drobovik_obrez['name'] in guns_shop:
                        drobovik_obrez_3 = f"<b>3 - {drobovik_obrez['name']}</b> - наносит от {drobovik_obrez['damage'][0]} до {drobovik_obrez['damage'][1]} очков урона\n" \
                                           f"Цена: {drobovik_obrez['price']} CR\n" \
                                           f"{'-' * 50}"
                        ikb_shop_guns_pick_3 = InlineKeyboardButton(text=f'3 ✅', callback_data=3)
                        drobovik_obrez_examination = True
                    else:
                        drobovik_obrez_3 = f"<b>3 - {drobovik_obrez['name']}</b> - наносит от {drobovik_obrez['damage'][0]} до {drobovik_obrez['damage'][1]} очков урона\n" \
                                           f"Распродано\n" \
                                           f"{'-' * 50}"
                        ikb_shop_guns_pick_3 = InlineKeyboardButton(text=f'3 ❎', callback_data=3)
                        drobovik_obrez_examination = False

                    data['examination_guns'] = {
                        'pistol_pmm_examination': pistol_pmm_examination,
                        'pistol_marta_examination': pistol_marta_examination,
                        'drobovik_obrez_examination': drobovik_obrez_examination

                    }



                    ikb_shop_guns_pick = InlineKeyboardMarkup(row_width=3).add(ikb_shop_guns_pick_1, ikb_shop_guns_pick_2,
                                                                            ikb_shop_guns_pick_3).add(
                            InlineKeyboardButton(text='Вернуться назад', callback_data='back_to_shop'))


                    await callback.message.edit_text(text=f"Выбирите оружие:\n"
                                                          f"Ваши сбережения: {await get_credit_balance(callback.from_user.id)} CR\n"
                                                          f"{pistol_pmm_1}\n"
                                                          f"{pistol_marta_2}\n"
                                                          f"{drobovik_obrez_3}\n"
                                                          f""
                                                          f"Для выбора нажмите на цифру",
                                                     parse_mode='html',
                                                     reply_markup=ikb_shop_guns_pick)
                    await FSMShop.next()

        elif callback.data == 'main_menu':
            async with state.proxy() as data:
                if callback.message.message_id != data['pick_shop_category']:
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





#@dp.callback_query_handler(state=FSMShop.buy_gun)
async def buying_gun(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:

        if callback.message.message_id != data['pick_shop_category']:
            await callback.answer(text='Сессия проходит вдругом меню', show_alert=True)
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            return

        # Пистолет ПМм
        elif callback.data == '1':
            if data['examination_guns']['pistol_pmm_examination']:
                if int(await get_credit_balance(callback.from_user.id)) >= pistol_pmm['price']:
                    await callback.message.edit_text(text=f"Вы уверены, что хотите купить {pistol_pmm['name']} за {pistol_pmm['price']} CR?",
                                                     reply_markup=ikb_shop_pick)
                    data['buy_gun'] = pistol_pmm['console_name']
                    data['accept_gun'] = pistol_pmm['price']
                    data['to_main_menu'] = pistol_pmm['name']
                    await FSMShop.next()
                else:
                    await callback.answer(text='Ваших сбережений не достаточно!')
                    return
            else:
                await callback.answer(text='У вас уже есть данное оружие!')

        # Пистолет Марта
        elif callback.data == '2':
            if data['examination_guns']['pistol_marta_examination']:
                if int(await get_credit_balance(callback.from_user.id)) >= pistol_marta['price']:
                    await callback.message.edit_text(
                        text=f"Вы уверены, что хотите купить {pistol_marta['name']} за {pistol_marta['price']} CR?",
                        reply_markup=ikb_shop_pick)
                    data['buy_gun'] = pistol_marta['console_name']
                    data['accept_gun'] = pistol_marta['price']
                    data['to_main_menu'] = pistol_marta['name']
                    await FSMShop.next()
                else:
                    await callback.answer(text='Ваших сбережений не достаточно!')
                    return
            else:
                await callback.answer(text='У вас уже есть данное оружие!')

        # Дробовик Обрез
        elif callback.data == '3':
            if data['examination_guns']['drobovik_obrez_examination']:
                if int(await get_credit_balance(callback.from_user.id)) >= drobovik_obrez['price']:
                    await callback.message.edit_text(
                        text=f"Вы уверены, что хотите купить {drobovik_obrez['name']} за {drobovik_obrez['price']} CR?",
                        reply_markup=ikb_shop_pick)
                    data['buy_gun'] = drobovik_obrez['console_name']
                    data['accept_gun'] = drobovik_obrez['price']
                    data['to_main_menu'] = drobovik_obrez['name']
                    await FSMShop.next()
                else:
                    await callback.answer(text='Ваших сбережений не достаточно!')
                    return
            else:
                await callback.answer(text='У вас уже есть данное оружие!')

        # Вернуться назад
        elif callback.data == 'back_to_shop':
            await shop_menu(callback, state)




#dp.callback_query_handler(state=FSMShop.accept_gun)
async def accept_shop_gun(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if callback.message.message_id != data['pick_shop_category']:
            await callback.answer(text='Сессия проходит вдругом меню', show_alert=True)
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            return

        elif callback.data == 'yes':
            await buy_gun(callback.from_user.id, data['buy_gun'])
            await minus_credit_balance(callback.from_user.id, data['accept_gun'])
            await callback.message.edit_text(text=f"Вы купили {data['to_main_menu']} за {data['accept_gun']} CR",
                                             reply_markup=ikb_return_to_main_menu)
            await FSMShop.next()

async def shop_guns_mn(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if callback.message.message_id != data['pick_shop_category']:
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




