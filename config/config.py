from environs import Env
from aiogram import Bot, Dispatcher

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
    bot: Bot = ctx['bot']
    await bot.session.close()

async def alert_deadline(ctx, chat_id, alert_type, subject, task):
    text = f'{alert_type}: {subject} - {task}'
    await bot.send_message(chat_id=chat_id, text=text)

class WorkerSettings():
    redis_settings = RedisSettings()
    on_startup = startup
    on_shutdown = shutdown
    functions = [alert_deadline,]

redis = Redis(host='localhost')
storage = RedisStorage(redis=redis) 
dp = Dispatcher(storage=storage)
