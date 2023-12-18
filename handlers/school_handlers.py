from aiogram.types import Message
from aiogram.filters import Command

from aiogram import Router
rt = Router()
#why can't i import this if it is located in states.py? impossible import from submodule to submodule?!

class Schedule():
    editing: bool = False
    creating: bool = False
    d = {'Понедельник':[], 'Вторник':[],'Среда':[],'Четверг':[],'Пятница':[],'Суббота':[],'Воскресенье':[]}
#and this???
def getlist_frommsg(text):
    text.replace(' ','').replace(',','').replace('.','')
    list = text.split(sep='\n')
    return list


schedule = Schedule()
i_to_day = {0: "Понедельник", 
                 1: "Вторник",
                 2: "Среда",
                 3: "Четверг",
                 4: "Пятница",
                 5: "Суббота",
                 6: "Воскресенье"}

@rt.message(Command(commands='newlesson_schedule'))
async def lesson_newschedule_command(msg: Message):
    await msg.answer(text='Начнем с понедельника. Присылай мне предметы на понедельник по порядку, обязательно каждый с новой строки')
    schedule.creating=True
    for i in range(7):
        await msg.answer(text=f'{i_to_day[i]}. Присылай уроки, обязательно каждый с новой строки')
        lesson_newschedule_process(msg, getlist_frommsg(msg.text),i)

@rt.message()
async def lesson_newschedule_process(msg: Message, lessonlist,dayi):
    if schedule.creating:
        schedule[i_to_day[dayi]] = lessonlist
        await msg.answer(f'Расписание на {i_to_day[dayi].lower()} успешно заполнен. Теперь {i_to_day[dayi+1].lower()}.')