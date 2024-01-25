from aiogram import Bot
import datetime
import sched
import time
import asyncio
import logging


logger = logging.getLogger(__name__)

bot_token = '6631562385:AAF4EyJbnHNCK0u1afPCuHHgFFz1uhmVg2o'
bot = Bot(token=bot_token)
async def alert_deadline(id, subject_task, due):
    text = 'ДЕДЛАЙН СЕГОДНЯ:\n'
    subject_task_formatted = subject_task
    due_formatted = due
    message = f'{text}{subject_task_formatted}: {due_formatted}'
    await bot.send_message(chat_id=id, text=message)
    

sch = sched.scheduler(time.monotonic,time.sleep)

async def schedule_deadline_alert(id,subject_task,due):
   logger.debug(msg=('New scheduled deadline_alert:\n\t'
                 f'{sch.enterabs(due,5,alert_deadline,argument=(id, subject_task, due))}'))
