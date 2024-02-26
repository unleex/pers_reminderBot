from aiogram import Bot
import logging
from datetime import timedelta
from environs import Env
logger = logging.getLogger(__name__)

env  = Env()
bot_token = env('BOT_TOKEN')
bot = Bot(token=bot_token)

async def schedule_deadline_alert(arqredis,chat_id,subject_task,due):
    logger.info(('Task notification queued.',
              await arqredis.enqueue_job('alert_deadline',chat_id, subject_task,_defer_by=timedelta(seconds=10)),
                     'Deferred until', due))