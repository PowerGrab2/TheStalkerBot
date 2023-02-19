from aiogram import types

from aiogram.utils import executor
from create_bot import dp, bot
from handlers import client, admin, other
from data_base import sqlite_db
from states.stateGuns import FSMMainMenu
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import Message, CallbackQuery


from aiogram.dispatcher.middlewares import BaseMiddleware



# ПРОВЕРКА НА РАБОТОСПОСОБНОСТЬ
async def on_startup(_):
    print('Бот был успешно запущен!')
    await sqlite_db.sql_start()


client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup)
