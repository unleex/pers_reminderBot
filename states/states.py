from aiogram.types import CallbackQuery
from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram.fsm.state import StatesGroup, State
redis = Redis(host='localhost')
storage = RedisStorage(redis=redis)

class FSMStates(StatesGroup):
    editing_schedule = State()
    editing_day = State()
    editing_tasks = State()
    adding_task = State()
    viewing_task = State()