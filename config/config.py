import os
from environs import Env

from aiogram import Bot

from aiogram.fsm.storage.redis import RedisStorage, Redis
from arq import create_pool
from arq.connections import RedisSettings
import asyncio

import logging
logger = logging.getLogger(__name__)

logger.info('aiogram logging started.')


env = Env()
env.read_env()
bot_token = env('BOT_TOKEN')
admin_id = env.int('ADMIN_ID')

bot = Bot(token=bot_token,
              parse_mode='HTML')

async def init_arqredis():
    arqredis = await create_pool(RedisSettings())
    return arqredis

arqredis = asyncio.run(init_arqredis())

redis = Redis(host='localhost')
storage = RedisStorage(redis=redis)