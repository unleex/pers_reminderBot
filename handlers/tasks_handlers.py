import sys, os
from pprint import pprint
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from aiogram.types import CallbackQuery, Message
from lexicon.lexicon import LEXICON_RU
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram import Router, F
from keyboards.tasks_keyboards import homework_kb_builder
from services.services import getdict_frommsg
from states.states import FSMStates
from my_typing.typing import schedule, new_homework, Homework
from keyboards.tasks_keyboards import add_task_kb
rt = Router()

days = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']
editdays = [f'edit{i}' for i in days]
viewdays = [f'view{i}' for i in days]
    


#tasks
@rt.callback_query(F.data=='edit_tasks',StateFilter(default_state))
async def tasks_menu(clb: CallbackQuery):
    await clb.message.answer(text=LEXICON_RU['edit_tasks_text'],
                             reply_markup=homework_kb_builder.as_markup(resize_keyboard=True))
    
#process
@rt.message(StateFilter(default_state,FSMStates.editing_tasks))
async def add_task(msg: Message, state: FSMContext):
    new_homework.subject_task, new_homework.due = getdict_frommsg(msg.text)
    subject: str = list(new_homework.subject_task.keys())[0].capitalize()#peculiar
    task: str = list(new_homework.subject_task.values())[0].capitalize()#same
    days_out = f'Записано на {"следующий урок" if new_homework.due == None else new_homework.due}'
    await msg.answer(text=f"Подтвердите ввод:\n{subject}: {task}. {days_out}",
                     reply_markup=add_task_kb)
    await state.set_state(FSMStates.adding_task)

#confirm
@rt.callback_query(F.data=='confirm_add_task',StateFilter(FSMStates.adding_task))
async def confirm_add_task(clb: CallbackQuery,state: FSMContext):
    schedule.tasks.append(new_homework)
    await clb.message.edit_text("Домашнее задание добавлено!")
    await state.clear()

#cancel
@rt.callback_query(F.data=='cancel_add_task',StateFilter(FSMStates.adding_task))
async def cancel_add_task(clb: CallbackQuery,state: FSMContext):
    new_homework.due=''
    new_homework.subject_task={}
    await clb.message.edit_text('Изменения отменены.')
    await state.clear()
