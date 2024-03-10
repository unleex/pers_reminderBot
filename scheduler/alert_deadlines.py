from aiogram import Bot

import logging
from environs import Env
from arq import ArqRedis
logger = logging.getLogger(__name__)

env  = Env()
bot_token = env('BOT_TOKEN')
bot = Bot(token=bot_token)

async def schedule_deadline_alert(arqredis: ArqRedis,chat_id,new_homework,due):
    logger.info(('Task notification queued.',
              await arqredis.enqueue_job('alert_deadline',chat_id, new_homework["subject"],new_homework["task"],
                    _defer_until=due),
                     'Deferred until', due))