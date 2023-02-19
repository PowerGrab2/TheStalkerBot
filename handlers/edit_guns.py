''' Механика оружий, есть ли у пользователя оружие находиться в sql таблице guns'''
from data_base.sqlite_db import have_gun, edit_current_gun, current_gun
from create_bot import bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from items.guns_items import *
from states.stateGuns import FSMChangeGun
from keyboards.client_kb import *
from data_base.sqlite_db import get_credit_balance
from states.stateGuns import FSMStalkerInfo, FSMMainMenu
from data_base.sqlite_db import exemination_username



#dp.callback_query_handler(text='edit_gun', state=FSMChangeGun.examination)
async def get_guns_inventory(callback: types.CallbackQuery, state: FSMContext):
    """Проверка на наличие оружия у пользователя"""
    await FSMChangeGun.examination.set()
    guns_inventory = []
    async with state.proxy() as data:
        data['examination'] = False
        # Проверка 'Есть ли инное оружие' ! True - добавить в инвентарь !
        if not data['examination']:
            if await have_gun(callback.from_user.id, pistol_pmm['console_name']):
                guns_inventory.append(pistol_pmm['name'])
            if await have_gun(callback.from_user.id, pistol_marta['console_name']):
                guns_inventory.append(pistol_marta['name'])
            if await have_gun(callback.from_user.id, drobovik_obrez['console_name']):
                guns_inventory.append(drobovik_obrez['name'])

            # Пистолет Пмм
            if pistol_pmm['name'] in guns_inventory:
                pistol_pmm_1 = f"<b>1 - {pistol_pmm['name']}</b> - наносит от {pistol_pmm['damage'][0]} до {pistol_pmm['damage'][1]} очков урона"
                pistol_pmm_examination = True
                ikb_edit_gun1 = InlineKeyboardButton(text='1 ✅', callback_data=1)
            else:
                pistol_pmm_1 = f"<b>1 - {pistol_pmm['name']}</b> - отсутствует"
                pistol_pmm_examination = False
                ikb_edit_gun1 = InlineKeyboardButton(text='1 ❎', callback_data=1)


            # Пистолет Марта
            if pistol_marta['name'] in guns_inventory:
                pistol_marta_2 = f"<b>2 - {pistol_marta['name']}</b> - наносит от {pistol_marta['damage'][0]} до {pistol_marta['damage'][1]} очков урона"
                pistol_marta_examination = True
                ikb_edit_gun2 = InlineKeyboardButton(text='2 ✅', callback_data=2)
            else:
                pistol_marta_2 = f"<b>2 - {pistol_marta['name']}</b> - отсутствует"
                pistol_marta_examination = False
                ikb_edit_gun2 = InlineKeyboardButton(text='2 ❎', callback_data=2)

            # Дробовик обрез
            if drobovik_obrez['name'] in guns_inventory:
                drobovik_obrez_3 = f"<b>3 - {drobovik_obrez['name']}</b> - наносит от {drobovik_obrez['damage'][0]} до {drobovik_obrez['damage'][1]} очков урона"
                drobovik_obrez_examination = True
                ikb_edit_gun3 = InlineKeyboardButton(text='3 ✅', callback_data=3)
            else:
                drobovik_obrez_3 = f"<b>3 - {drobovik_obrez['name']}</b> - отсутствует"
                drobovik_obrez_examination = False
                ikb_edit_gun3 = InlineKeyboardButton(text='3 ❎', callback_data=3)

            data['examination'] = {
                'pistol_pmm_examination': pistol_pmm_examination,
                'pistol_marta_examination': pistol_marta_examination,
                'drobovik_obrez_examination': drobovik_obrez_examination

            }

            data['edit_gun'] = callback.message.message_id




            ikb_edit_gun = InlineKeyboardMarkup(row_width=3,
                                                inline_keyboard=[
                                                    [ikb_edit_gun1, ikb_edit_gun2, ikb_edit_gun3],
                                                    [InlineKeyboardButton(text='Вернуться назад', callback_data='back_to_info_about_stalker')]
                                                ])


            await callback.message.edit_text(text=f"Выбирите оружие:\n"
                                        f"{pistol_pmm_1}\n"
                                        f"{pistol_marta_2}\n"
                                        f"{drobovik_obrez_3}\n"
                                        f""
                                        f"Для выбора нажмите на цифру",
                                   parse_mode='html',
                                   reply_markup=ikb_edit_gun)



            await FSMChangeGun.next()

#@dp.callback_query_handler(state=FSMChangeGun.edit_gun)
async def set_current_gun(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:


        if callback.message.message_id != data['edit_gun']:
            await callback.answer(text='Сессия проходит вдругом меню', show_alert=True)
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            return



        if callback.data == '1':
            if (await current_gun(callback.from_user.id))['console_name'] != pistol_pmm['console_name']:
                if int(data['examination']['pistol_pmm_examination']):
                    await edit_current_gun(callback.from_user.id, pistol_pmm['console_name'])
                    await callback.message.edit_text(text=f"Ваше текущее оружие: {(await current_gun(callback.from_user.id))['name']}",
                                                     reply_markup=ikb_return_to_main_menu)
                    await FSMChangeGun.next()
                else:
                    await callback.answer(text='У вас нет данного оружия,\n'
                                          'Вы можете купить его в торговой лавке')
                    await FSMChangeGun.edit_gun.set()
            else:
                await callback.answer(text='Это ваше текущее оружие')
                await FSMChangeGun.edit_gun.set()

        elif callback.data == '2':
            if (await current_gun(callback.from_user.id))['console_name'] != pistol_marta['console_name']:
                if int(data['examination']['pistol_marta_examination']):
                    await edit_current_gun(callback.from_user.id, pistol_marta['console_name'])
                    await callback.message.edit_text(
                        text=f"Ваше текущее оружие: {(await current_gun(callback.from_user.id))['name']}",
                        reply_markup=ikb_return_to_main_menu)
                    await FSMChangeGun.next()
                else:
                    await callback.answer(text='У вас нет данного оружия,\n'
                                               'Вы можете купить его в торговой лавке')
                    await FSMChangeGun.edit_gun.set()
            else:
                await callback.answer(text='Это ваше текущее оружие')
                await FSMChangeGun.edit_gun.set()

        elif callback.data == '3':
            if (await current_gun(callback.from_user.id))['console_name'] != drobovik_obrez['console_name']:
                if int(data['examination']['drobovik_obrez_examination']):
                    await edit_current_gun(callback.from_user.id, drobovik_obrez['console_name'])
                    await callback.message.edit_text(
                        text=f"Ваше текущее оружие: {(await current_gun(callback.from_user.id))['name']}",
                        reply_markup=ikb_return_to_main_menu)
                    await FSMChangeGun.next()
                else:
                    await callback.answer(text='У вас нет данного оружия,\n'
                                               'Вы можете купить его в торговой лавке')
                    await FSMChangeGun.edit_gun.set()
            else:
                await callback.answer(text='Это ваше текущее оружие')
                await FSMChangeGun.edit_gun.set()

        elif callback.data == 'back_to_info_about_stalker':


            await state.finish()
            await callback.message.edit_text(text=f"Твои сбережения: {await get_credit_balance(callback.from_user.id)}\n"
                                                  f"Твое оружие: {(await current_gun(callback.from_user.id))['name']}",
                                             reply_markup=ikb_stalker_info)
            await exemination_username(user_id=callback.from_user.id,
                                       user_name=callback.from_user.username,
                                       name=callback.from_user.first_name)

            async with state.proxy() as data:
                data['info'] = callback.message.message_id
                await FSMStalkerInfo.pick_category.set()

async def to_mn_edit_gun(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if callback.message.message_id != data['edit_gun']:
            await callback.answer(text='Сессия проходит в другом меню', show_alert=True)
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            return
        data['*'] = callback.message.message_id

        await state.finish()
        await callback.message.edit_text(text="Добро пожаловать, сталкер\n"
                                              f"Рад тебя снова видеть, чем займешься?\n"
                                              f"/start",
                                         reply_markup=kb_main_menu)
        await FSMMainMenu.wait_message.set()
