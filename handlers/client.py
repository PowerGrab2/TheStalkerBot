# Импорты
import asyncio

from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext

from config import TheStalker
from create_bot import bot, dp
from data_base.sqlite_db import sql_create_profile, get_credit_balance, minus_credit_balance, plus_credit_balance, \
    exemination_username, current_gun
from handlers.edit_guns import get_guns_inventory, set_current_gun, to_mn_edit_gun
from handlers.outing import outing_menu, outing_locations, pick_current_location, get_ivent_answer, register_outing_handlers
from handlers.shop import shop_menu, gun_shop_examination, buying_gun, accept_shop_gun, shop_guns_mn
from keyboards.client_kb import ikb_client_kubiki_number, kb_main_menu, ikb_stalker_info
from states.stateGuns import *
from states.stateGuns import FSMShop
import random
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler

sheduler = AsyncIOScheduler(timezone="Europe/Kyiv")

async def pre_start_cmd(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == '/start':
            data['*'] = message.message_id + 1
            await start_command(message, state)
        else:
            await message.delete()


async def start_command(message: types.Message, state: FSMContext):
    ''' Команда запуска бота '''
    MainMenuText = random.choice([f"<i>О, <b>{message.from_user.first_name}</b>, рад, что ты вернулся! Мы уже успели соскучиться, Василий даже переживать начал. Куда отправишься?👣\n\n</i>", f"<i><b>Сталкер?</b> Ты снова здесь? И куда же ты собрался?\n{'-' * 50}</i>", \
        f"<i>Да ладно! <b>Ты все же вернулся</b>, но на долго ли?\n{'-' * 50}</i>"])
    IntrestingFact = random.choice([f"<i><b>▶️ Интересный факт: бота создал человек, который не любит сталкеров ◀️</b></i>"])
    

    if message.text == '/start':
        await bot.send_message(chat_id=message.from_user.id,
                                text=MainMenuText + IntrestingFact,
                                reply_markup=kb_main_menu,
                                parse_mode='html')

        await sql_create_profile(user_id=message.from_user.id,
                                    user_name=message.from_user.username,
                                    name=message.from_user.first_name)
        await message.delete()
    else:
        await message.delete()
        print('f')
    await FSMMainMenu.wait_message.set()


async def wait_category_mn(callback: types.CallbackQuery, state: FSMContext):
    '''Выбираем категорию'''
    async with state.proxy() as data:
        async with state.proxy() as data:
            if callback.message.message_id != data['*']:
                await callback.answer(text='Сессия проходит вдругом меню', show_alert=True)
                await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
                return

        if callback.data == 'info_about_stalker':
            await state.finish()
            await stalker_info(callback, state)
        elif callback.data == 'shop':
            await state.finish()
            await shop_menu(callback, state)
        elif callback.data == 'outing':
            await state.finish()
            await outing_menu(callback, state)


async def stalker_info(callback: types.CallbackQuery, state: FSMContext):
    '''Информация о сталкере'''

    await callback.message.edit_text(text=f"Твои сбережения: {await get_credit_balance(callback.from_user.id)}\n"
                                          f"Текущее оружие: {(await current_gun(callback.from_user.id))['name']}",
                                     reply_markup=ikb_stalker_info)
    await exemination_username(user_id=callback.from_user.id,
                               user_name=callback.from_user.username,
                               name=callback.from_user.first_name)

    async with state.proxy() as data:
        data['info'] = callback.message.message_id
        await FSMStalkerInfo.pick_category.set()


async def stalker_get_category(callback: types.CallbackQuery, state: FSMContext):
    '''Получаем калбек из Информация о сталкере'''
    async with state.proxy() as data:
        if callback.message.message_id != data['info']:
            await callback.answer(text='Сессия проходит в другом меню', show_alert=True)
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            return

        if callback.data == 'edit_gun':
            await state.finish()
            await get_guns_inventory(callback, state)

        elif callback.data == 'main_menu':
            await state.finish()
 

            await callback.message.edit_text(text="Добро пожаловать, сталкер\n"
                                                  f"Рад тебя снова видеть, чем займешься?\n"
                                                  f"/start",
                                             reply_markup=kb_main_menu)

            await FSMMainMenu.wait_message.set()
            data['*'] = callback.message.message_id

        elif callback.data == 'edit_costume':
            await callback.answer('Эта функция недоступна', show_alert=True)
            return


def register_handlers_client(dp: Dispatcher):
    '''Регистрация Хендлеров'''
    
    
    # Стартовая команда
    dp.register_message_handler(pre_start_cmd, state='*')
    dp.register_message_handler(start_command, state='*')

    # Менюшка !
    dp.register_callback_query_handler(wait_category_mn, state=FSMMainMenu.wait_message)

    # Информация о сталкере
    dp.register_callback_query_handler(stalker_info, text='info_about_stalker', state=FSMStalkerInfo.info)
    dp.register_callback_query_handler(stalker_get_category, state=FSMStalkerInfo.pick_category)
    dp.register_callback_query_handler(get_guns_inventory, state=FSMChangeGun.examination)
    dp.register_callback_query_handler(set_current_gun, state=FSMChangeGun.edit_gun)
    dp.register_callback_query_handler(to_mn_edit_gun, state=FSMChangeGun.to_the_mn)

    # Торговая лавка
    dp.register_callback_query_handler(shop_menu, text='shop', state=FSMShop.examination_guns)
    dp.register_callback_query_handler(gun_shop_examination, state=FSMShop.pick_shop_category)
    dp.register_callback_query_handler(buying_gun, state=FSMShop.buy_gun)
    dp.register_callback_query_handler(accept_shop_gun, state=FSMShop.accept_gun)
    dp.register_callback_query_handler(shop_guns_mn, state=FSMShop.to_main_menu)

    # Отправиться на вылазку
    register_outing_handlers(dp)

