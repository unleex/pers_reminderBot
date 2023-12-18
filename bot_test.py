import os
from environs import Env
import dotenv
env = Env()
env.read_env()
bot_token = env('BOT_TOKEN')
admin_id = env.int('ADMIN_ID')
print(os.getenv('BOT_TOKEN'))   
print(os.getenv('ADMIN_ID'))


import asyncio
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
from aiogram import Router, F,Dispatcher,Bot
from keyboards.set_menu import set_main_menu
rt = Router()
dp = Dispatcher()
#change dp to rt
#include router





async def main() -> None:
    bot = Bot(token=bot_token,
              parse_mode='HTML')
    await set_main_menu(bot)
    await dp.start_polling(bot)
if __name__ == '__main__':
    asyncio.run(main())