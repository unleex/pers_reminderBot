from aiogram.types import CallbackQuery
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
storage = MemoryStorage()

class Schedule:
    week_schedule={'Понедельник': ['Здесь пока пусто('],'Вторник':['Здесь пока пусто('],'Среда':['Здесь пока пусто('],'Четверг':['Здесь пока пусто('],'Пятница':['Здесь пока пусто('],'Суббота':['Здесь пока пусто('],'Воскресенье':['Здесь пока пусто(']}
    new_schedule={}
    clb: CallbackQuery
schedule = Schedule()
class Homework:
    subject: str
    due: int#unix time
    task: str

class FSMStates(StatesGroup):
    editing_schedule = State()
    editing_day = State()