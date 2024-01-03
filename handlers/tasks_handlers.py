import sys
import os


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from aiogram.types import CallbackQuery, Message
from lexicon.lexicon import LEXICON_RU
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router, F
from keyboards.tasks_keyboards import homework_kb_builder
from states.states import FSMStates
from services.services import getdict_frommsg
from my_typing.typing import new_homework,schedule
from keyboards.tasks_keyboards import adding_task_kb
rt = Router()

days = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']
editdays = [f'edit{i}' for i in days]
viewdays = [f'view{i}' for i in days]
    


#tasks
@rt.callback_query(F.data=='edit_tasks',StateFilter(default_state))
async def tasks_menu(clb: CallbackQuery,state: FSMContext):
    await clb.message.answer(text=LEXICON_RU['edit_tasks_text'],
                             reply_markup=homework_kb_builder.as_markup(resize_keyboard=True))
    await state.set_state(FSMStates.editing_tasks)

@rt.message(StateFilter(default_state,FSMStates.editing_tasks))
async def add_task_command(msg: Message,state: FSMContext):
    out = 'Подтвердите ввод:\n'
    day_out='Записано на следующий урок'
    outlist = getdict_frommsg(msg.text)
    if outlist[1] != None:
        day_out = f'Записано на {outlist[1]}'
    subject = list(outlist[0].keys())[0]
    task = list(outlist[0].values())[0]
    out += f'{subject}:'
    out += f'{task}\n'
    out += day_out
    print(outlist, 'PRE HW')
    new_homework.subject_task=outlist[0]
    new_homework.due = outlist[1]
    await msg.answer(out,reply_markup=adding_task_kb)
    await state.set_state(FSMStates.adding_task)

@rt.callback_query(F.data == 'confirm_add_task',StateFilter(FSMStates.adding_task))
async def confirm_add_task(clb: CallbackQuery,state:FSMContext):
    schedule.tasks.append(new_homework)
    print(new_homework.subject_task,new_homework.due,'NEW HW')
    new_homework.subject_task={}
    new_homework.due={}
    print([i.subject_task for i in schedule.tasks], 'ADDED HW')
    await clb.message.edit_text('Задача добавлена!')
    await state.clear()
    attrs = []
    for task in schedule.tasks:
        attrs.append([task.subject_task, task.due])
    print(attrs)

@rt.callback_query(F.data == 'cancel_add_task',StateFilter(FSMStates.adding_task))
async def cancel_add_task(clb: CallbackQuery,state:FSMContext):
    new_homework.subject_task={}
    new_homework.due=''
    await clb.message.edit_text('Изменения отменены')
    await state.clear()
