import datetime
import json
from services.services import values, flatten_list
from aiogram import Router, Bot
from aiogram.methods import send_message
from main import bot_token

bot = Bot(token=bot_token, parse_mode='HTML')
rt = Router()
'CREATE DEADLINES LIST'
with open('users.json', 'r') as f:
  data = json.load(f)
  

async def alert_deadline(data):
  date_time = str(datetime.datetime.today()).split()
  date_time[1] = date_time[1][:date_time[1].rfind('.')]
  for chat_id in values(data):
      for task in values(chat_id['tasks']):
        if task['deadline'] == date_time:
            await bot.send_message(chat_id=chat_id, text=f'ДЕДЛАЙН СЕГОДНЯ: {task}')
    