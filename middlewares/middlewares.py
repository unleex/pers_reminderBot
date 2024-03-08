from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject, User

from typing import Callable, Any
import json
import logging
from environs import Env
env = Env()
logger = logging.getLogger(__name__)
class DataBaseAccessor(BaseMiddleware):
    async def __call__(self, 
                       handler: Callable, 
                       event: TelegramObject, 
                       data: dict[str,Any]) -> Any:

        user: User = data['event_from_user']

        if user is None:
            return await handler(event, data)
        
        with open('db/db.json', mode='r') as fp:
            db: dict = json.load(fp)
        
        if str(user.id) in db.keys():
            data['user_db'] =  db[str(user.id)]

        result = await handler(event, data)


        return result