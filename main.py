#logging
import logging.config
import yaml
with open('logging_config/logging_config.yaml', 'rt') as f:
    logging_config = yaml.safe_load(f.read())
logging.config.dictConfig(logging_config)

import config.config

####
import asyncio
import logging
import json

from config.config import dp
from keyboards.set_menu import set_main_menu
from arq.connections import create_pool, RedisSettings

from handlers import other_handlers,tasks_handlers,schedule_handlers,edit_days_handlers
from middlewares import middlewares

logger = logging.getLogger(__name__)


async def main() -> None:
    bot = config.config.bot
    
    dp.include_router(schedule_handlers.rt)
    dp.include_router(edit_days_handlers.rt)
    dp.include_router(tasks_handlers.rt)
    dp.include_router(other_handlers.rt)

    dp.update.middleware(middlewares.DataBaseAccessor())
    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates = True)

    logger.info("AAAND we're online")

    await dp.start_polling(bot,
                           arqredis = await create_pool(RedisSettings),
                           user_db = json.load(open('db/db.json','r'))) 

if __name__ == '__main__':
    asyncio.run(main()) 