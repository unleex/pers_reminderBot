from aiogram.fsm.state import StatesGroup, State
days = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']
class FSMStates(StatesGroup):
    editing_schedule = State()
    editing_day = State()
    editing_tasks = State()
    adding_task = State()
    viewing_task = State()
    viewing_schedule= State()
    viewing_day = State()
