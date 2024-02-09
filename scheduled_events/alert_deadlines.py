from aiogram import Bot
import datetime
import arq
import time
import asyncio
import logging
from config.config import arqredis
logger = logging.getLogger(__name__)

bot_token = '6631562385:AAF4EyJbnHNCK0u1afPCuHHgFFz1uhmVg2o'
bot = Bot(token=bot_token)

async def alert_deadline(id, subject_task, due):

    text = 'ДЕДЛАЙН СЕГОДНЯ:\n'
    message = f'{text}{subject_task}: {due}'
    await bot.send_message(chat_id=id, text=message)
    
async def schedule_deadline_alert(id,subject_task,due):
    alert_deadline_task = asyncio.create_task(alert_deadline(id,subject_task,due))
    logger.info(('Task notification queued.',
              await arqredis.enqueue_job('alert_deadline_task',_defer_until=due),
                     'Deferred until', due))