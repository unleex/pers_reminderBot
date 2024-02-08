#config
import config.config
import logging.config
import yaml
with open('logging_config/logging_config.yaml', 'rt') as f:
    logging_config = yaml.safe_load(f.read())
logging.config.dictConfig(logging_config)
####

import asyncio
import logging
from aiogram import Bot
from create_dp import dp
from keyboards.set_menu import set_main_menu


from handlers import schedule_handlers, edit_days_handlers, service_handlers, tasks_handlers

import scheduled_events.alert_deadlines as alert_deadlines

logging.info("AAAND we're online")

async def main() -> None:
    bot = config.config.bot
    
    dp.include_router(service_handlers.rt)
    dp.include_router(tasks_handlers.rt)
    dp.include_router(edit_days_handlers.rt)
    dp.include_router(schedule_handlers.rt)

    await set_main_menu(bot)

    await bot.delete_webhook(drop_pending_updates=1)
    await dp.start_polling(bot)

    redis = config.config.redis
    storage = config.config.storage


if __name__ == '__main__':
    asyncio.run(main()) 