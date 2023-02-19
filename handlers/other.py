from aiogram import types, Dispatcher
from create_bot import dp

async def no_start(message: types.Message):
    if message.text != '/start':
        await message.delete()



def register_handlers_other(dp: Dispatcher):
    #dp.register_message_handler(no_start, state='*')
    pass
