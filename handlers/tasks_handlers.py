import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery, Message,InlineKeyboardButton,InlineKeyboardMarkup
from lexicon.lexicon import LEXICON_RU
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router, F
from keyboards.tasks_keyboards import homework_kb_builder,homework_service_butts
from states.states import FSMStates
from services.services import getdict_frommsg,gen_tasks_inline_kb,are_equal,format_due
from my_typing.typing import new_homework,schedule,Homework
from keyboards.tasks_keyboards import adding_task_kb
from scheduled_events.alert_deadlines import schedule_deadline_alert
rt = Router()

import logging

logger = logging.getLogger(__name__)

days = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']
editdays = [f'edit{i}' for i in days]
viewdays = [f'view{i}' for i in days]
    


#tasks
@rt.callback_query(F.data=='edit_tasks',StateFilter(default_state))
async def tasks_menu(clb: CallbackQuery,state: FSMContext):
    homework_kb_builder.row(*gen_tasks_inline_kb(schedule.tasks),width=1)
    homework_kb_builder.row(*homework_service_butts,width=1)
    await clb.message.answer(text=LEXICON_RU['edit_tasks_text'],
                             reply_markup=homework_kb_builder.as_markup(resize_keyboard=True))
    await state.set_state(FSMStates.editing_tasks)

#add task
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
    new_homework.subject_task=outlist[0]
    new_homework.due = outlist[1]
    await msg.answer(out,reply_markup=adding_task_kb)
    await state.set_state(FSMStates.adding_task)

#confirm adding task
@rt.callback_query(F.data == 'confirm_add_task',StateFilter(FSMStates.adding_task))
async def confirm_add_task(clb: CallbackQuery,state:FSMContext):
    schedule.tasks.append(Homework(subject_task=new_homework.subject_task,
                                   due = new_homework.due))
    new_homework.subject_task={}
    new_homework.due={}
    deadline = format_due(new_homework.due)
    await schedule_deadline_alert(clb.from_user.id,new_homework.subject_task,new_homework.due)
    await clb.message.edit_text('Задача добавлена!')
    await state.clear()

    logger.debug('Новая задача добавлена.\n', clb.from_user.id,new_homework.subject_task,new_homework.due)

#cancel adding task
@rt.callback_query(F.data == 'cancel_add_task',StateFilter(FSMStates.adding_task))
async def cancel_add_task(clb: CallbackQuery,state:FSMContext):
    new_homework.subject_task={}
    new_homework.due=''
    await clb.message.edit_text('Изменения отменены.')
    await state.clear()

#view task
@rt.callback_query(F.data.startswith('tasks:'),StateFilter(FSMStates.editing_tasks))
async def view_task_command(clb: CallbackQuery, state : FSMContext):
    complete = InlineKeyboardButton(
        text='✅Выполнено',
        callback_data='complete:'+clb.data
    )
    to_menu = InlineKeyboardButton(
        text='⬅️В задания',
        callback_data='to_tasks')
    inlkb = InlineKeyboardMarkup(
        inline_keyboard=[[complete],
                         [to_menu]],
        resize_keyboard=True
    )
    await clb.message.edit_text(text=clb.data[6:clb.data.rfind(':')],
                                reply_markup=inlkb)
    await state.set_state(FSMStates.viewing_task)

#complete task
@rt.callback_query(F.data.startswith('complete:'),
                   StateFilter(FSMStates.viewing_task, FSMStates.editing_tasks)
)
async def complete_task(clb: CallbackQuery,state: FSMContext):
    norm_data = clb.data[15:]#англ:стр 15 номер 1:пн
    subject, task, due = norm_data.split(sep=':')
    if due == '':
        due = None
    completed_task = Homework(subject_task={subject: task}, due=due)

    for target_task in schedule.tasks:
        if are_equal(completed_task, target_task):#error
            schedule.tasks.remove(target_task)
            homework_kb_builder.from_markup() #avoid duplication
            homework_kb_builder.row(*gen_tasks_inline_kb(schedule.tasks),width=1)
            homework_kb_builder.row(*homework_service_butts,width=1)
            await clb.message.edit_text(text='Задание выполнено!',
                                        reply_markup=homework_kb_builder.as_markup(
                                            resize_keyboard=True
                                        ))
            await state.set_state(FSMStates.editing_tasks)
            logging.debug('Successfully completed task:\n', subject,task,due)
    await clb.message.edit_text(
        "Couldn't find task to complete. Idk why, really..")
    await state.set_state(FSMStates.editing_tasks)
    logging.error('Could not compare '
                  f'Homework({completed_task.subject_task}, {completed_task.due}) ' 
                  f'and Homework({target_task.subject_task}, {target_task.due}')