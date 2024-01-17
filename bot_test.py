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
import datetime
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram import Router, F,Dispatcher,Bot
from keyboards.set_menu import set_main_menu
from services.services import values
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

# def check_deadlines(func):
#    def wrapper(data):
#       func(*args, **kwargs)
#    return wrapper
    
# @check_deadlines
async def alert_deadline(data): 
  print('success!1')
  bot = Bot(token=bot_token,
              parse_mode='HTML')
  date_time = str(datetime.datetime.today()).split()
  date_time[1] = date_time[1][:date_time[1].rfind('.')]
  for chat_id in values(data):
      for task in values(chat_id['tasks']):
        if task['deadline'] == date_time:
            await print('success!')#bot.send_message(chat_id=chat_id, text=f'ДЕДЛАЙН СЕГОДНЯ: {task}')
        
