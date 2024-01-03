#config
import os
from environs import Env
env = Env()
env.read_env()
bot_token = env('BOT_TOKEN')
admin_id = env.int('ADMIN_ID')
print(os.getenv('BOT_TOKEN'))   
print(os.getenv('ADMIN_ID'))
from handlers import schedule_handlers, edit_days_handlers, service_handlers, tasks_handlers
####

import asyncio
from aiogram import Bot
from create_dp import dp
from keyboards.set_menu import set_main_menu
from aiogram.fsm.storage.redis import RedisStorage, Redis
async def main() -> None:
    bot = Bot(token=bot_token,
              parse_mode='HTML')
    dp.include_router(service_handlers.rt)
    dp.include_router(tasks_handlers.rt)
    dp.include_router(edit_days_handlers.rt)
    dp.include_router(schedule_handlers.rt)
    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=1)
    await dp.start_polling(bot)
    redis = Redis(host='localhost')
    storage = RedisStorage(redis=redis)
if __name__ == '__main__':
    asyncio.run(main())