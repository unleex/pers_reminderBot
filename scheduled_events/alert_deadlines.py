from aiogram import Bot
import datetime
import arq
import time
import asyncio
import logging
from arq import create_pool
from arq.connections import RedisSettings


logger = logging.getLogger(__name__)

bot_token = '6631562385:AAF4EyJbnHNCK0u1afPCuHHgFFz1uhmVg2o'
bot = Bot(token=bot_token)
async def alert_deadline(id, subject_task, due):

    text = 'ДЕДЛАЙН СЕГОДНЯ:\n'
    subject_task_formatted = subject_task
    due_formatted = due
    message = f'{text}{subject_task_formatted}: {due_formatted}'
    await bot.send_message(chat_id=id, text=message)
    
async def schedule_deadline_alert(id,subject_task,due):
	redis = await create_pool(RedisSettings())

	alert_deadline_task = asyncio.create_task(alert_deadline(id,subject_task,due))
	redis.enqueue_job('alert_deadline_task',_defer_until=due)