#config
import os
from environs import Env
env = Env()
env.read_env()
bot_token = env('BOT_TOKEN')
admin_id = env.int('ADMIN_ID')
print(os.getenv('BOT_TOKEN'))   
print(os.getenv('ADMIN_ID'))
from handlers import school_handlers, info_handlers
####

import asyncio
from aiogram import Bot, Dispatcher
from create_dp import dp
from aiogram.types import BotCommand
from keyboards.set_menu import set_main_menu

async def main() -> None:
    bot = Bot(token=bot_token,
              parse_mode='HTML')
    dp.include_router(info_handlers.rt)
    dp.include_router(school_handlers.rt)
    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=1)
    await dp.start_polling(bot)
if __name__ == '__main__':
    asyncio.run(main())

