from environs import Env
import os
from aiogram import Bot

from aiogram.fsm.storage.redis import RedisStorage, Redis
from arq.connections import RedisSettings

import logging
logger = logging.getLogger(__name__)

logger.info('aiogram logging started.')


env = Env()
env.read_env()
bot_token = env('BOT_TOKEN')
admin_id = env.int('ADMIN_ID')

bot = Bot(token=bot_token,
              parse_mode='HTML')

async def startup(ctx):
    ctx['bot'] = Bot(token = bot_token)

async def shutdown(ctx):
    await ctx['bot'].session.close()

async def alert_deadline(ctx, chat_id, subject_task):
    bot: Bot = ctx['bot']
    text = f'ДЕДЛАЙН: {subject_task}'
    await bot.send_message(chat_id=chat_id, text=text)

class WorkerSettings():
    redis_settings = RedisSettings()
    on_startup = startup
    on_shutdown = shutdown
    functions = [alert_deadline,]

redis = Redis(host='localhost')
storage = RedisStorage(redis=redis)

#os.system('arq config.config.WorkerSettings')