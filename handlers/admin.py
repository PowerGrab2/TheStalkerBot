from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot
from data_base.sqlite_db import is_admin_function, plus_credit_balance, minus_credit_balance, get_credit_balance
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text


async def give_credits_cmd(message: types.Message):
    if await is_admin_function(message.from_user.id) == 1:
        if message.reply_to_message:
            if len(message.text.split(' ')) == 2 and message.text.split(' ')[1].isdigit():
                await plus_credit_balance(message.reply_to_message.from_user.id, message.text.split(' ')[1])
                await message.delete()
            else:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Некоректные данные, введите /give {число}\n'
                                            'Пример: /give 1000')
        else:
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Эта команда должна быть ответом на сообщение!')
    else:
        await message.reply(text='Эта команда для админов!')


async def null_credits_cmd(message: types.Message):
    if await is_admin_function(message.from_user.id) == 1:
        if not message.reply_to_message:
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Эта команда должна быть ответом на сообщение!')
        else:
            await minus_credit_balance(message.reply_to_message.from_user.id, await get_credit_balance(message.reply_to_message.from_user.id))
            await message.reply_to_message.reply(text='Ваши кредиты были сброшены')
            await message.delete()
    else:
        await message.reply(text='Эта команда для админов!')












def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(give_credits_cmd, commands=['give'])
    dp.register_message_handler(null_credits_cmd, Text(equals=['Обнулить', '/null'], ignore_case=True))