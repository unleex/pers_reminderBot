from aiogram.types import CallbackQuery
from aiogram.filters.callback_data import CallbackData

class Homework:
    subject_task: dict
    due: str#make to unix time
new_homework=Homework()

class Schedule:
    week_schedule={'Понедельник': ['Здесь пока пусто('],'Вторник':['Здесь пока пусто('],'Среда':['Здесь пока пусто('],'Четверг':['Здесь пока пусто('],'Пятница':['Здесь пока пусто('],'Суббота':['Здесь пока пусто('],'Воскресенье':['Здесь пока пусто(']}
    new_schedule={}
    clb: CallbackQuery
    tasks: list[Homework]
    tasks=[]
schedule = Schedule()

class TasksCallbackFactory(CallbackData, prefix='tasks'):
    subject: str
    task: str
    due: str