import sys
import os
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery, Message, Message,InlineKeyboardButton,InlineKeyboardMarkup
from lexicon.lexicon import LEXICON_RU
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram import Router, F

from datetime import datetime

from keyboards.tasks_keyboards import homework_service_butts
from states.states import FSMStates
from services.services import (find_and_replace,
                               normalize_duedate,get_time_frommsg,get_day_frommsg,keys)
from keyboards.tasks_keyboards import adding_task_kb
from states.states import FSMStates
from scheduler.alert_deadlines import schedule_deadline_alert
from arq import ArqRedis
from filters.filters import IsTaskFormat

rt = Router()

import logging

logger = logging.getLogger(__name__)

days = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']
editdays = [f'edit{i}' for i in days]
viewdays = [f'view{i}' for i in days]
DEFAULT_DEADLINE_TIME: tuple = (9,00)


#tasks
@rt.callback_query(F.data=='edit_tasks',StateFilter(default_state))
async def tasks_menu(clb: CallbackQuery,state: FSMContext,user_db: dict):

    homeworks = user_db["homeworks"]
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton]
    for homework in homeworks:
        print(keys(homework)[0])
        buttons.append(InlineKeyboardButton(text=
                                            f'{homework["subject"]} - {homework["task"]}',
                                            callback_data=keys(homework)[0]))
    kb_builder.row(*buttons,width=1)
    kb_builder.row(*homework_service_butts,width=1)
    await clb.message.answer(text=LEXICON_RU['tasks_menu'],
                             reply_markup=kb_builder.as_markup(resize_keyboard=True))
    await state.set_state(FSMStates.editing_tasks)

#add task
@rt.message(IsTaskFormat(),StateFilter(default_state,FSMStates.editing_tasks))
async def add_task_command(msg: Message,state: FSMContext,user_db: dict):
    text = msg.text
    out = 'Подтвердите ввод:\n'
    day_out='Записано на следующий урок'

    #extract deadline and leave only text with subject and task
    due_time = get_time_frommsg(text)
    if due_time == (None, None):
        due_time = DEFAULT_DEADLINE_TIME
    due_day = get_day_frommsg(text)

    text = find_and_replace(text, str(due_time[0]), '')
    text = find_and_replace(text, str(due_time[1]), '')
    text = find_and_replace(text, str(due_day), '')
    text = find_and_replace(text, ':', '')

    subject = text[:text.find("-")].strip().capitalize()
    task = text[text.find("-")+1:].strip().capitalize()

    out += f'{subject}:'
    out += f'{task}\n'
    out += day_out

    if due_day:
        due_date = normalize_duedate(due_day)
        out = f'Записано на {due_day}'

    user_db["homeworks"].update(
        {'Unconfirmed homework': {
            "subject": subject,
            "task": task,
            "duedate": due_date,
            "duetime": due_time}
        }
    )
    
    await msg.answer(out,reply_markup=adding_task_kb)
    await state.set_state(FSMStates.adding_task)

#confirm adding task
@rt.callback_query(F.data == 'confirm_add_task',StateFilter(FSMStates.adding_task))
async def confirm_adding_task(clb: CallbackQuery,state:FSMContext,arqredis: ArqRedis,user_db):
    try:
        new_homework: dict = user_db["homeworks"]['Unconfirmed homework']
    
    except KeyError:
        await clb.message.edit_text('Неизвестная ошибка. ')
        await state.clear()
        return
    if new_homework["dueday"]:

        #add 2000 to year because it decreases to tens(2024->24)
        new_homework["duedate"][0] += 2000
        due_datetime = datetime(*new_homework["duedate"],*new_homework["duetime"])
        await schedule_deadline_alert(arqredis,clb.from_user.id,new_homework,due_datetime)

    logger.info(msg=(f'New homework added.\n\t'
            f'User: {clb.from_user.id}\t'
            f'Subject: {new_homework["subject"]}\t' 
            f'Task: {new_homework["subject"]}\t'
            f'Deadline: {due_datetime}'))
    #Homework_{msg.from_user.id}_{datetime.today().strftime("%Y/%m/%d_%H:%M%S")}
    await clb.message.edit_text('Задача добавлена!')
    await state.clear()


#cancel adding task
@rt.callback_query(F.data == 'cancel_add_task',StateFilter(FSMStates.adding_task))
async def cancel_add_task(clb: CallbackQuery,state:FSMContext,user_db: dict):

    del user_db["homeworks"]["Unconfirmed homework"]
    await clb.message.edit_text('Изменения отменены.')
    await state.clear()

#view task
@rt.callback_query(F.data.startswith('Homework_'),StateFilter(FSMStates.editing_tasks))
async def view_task_command(clb: CallbackQuery, state : FSMContext,user_db: dict):
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
    try:
        task = user_db["homeworks"][clb]
        await clb.message.edit_text(text=f'{task["subject"]} - {task["task"]}',
                                reply_markup=inlkb)
        await state.set_state(FSMStates.viewing_task)

    except KeyError:
        await clb.message.edit_text(text='Неизвестная ошибка.')
        state.clear()

#complete task
@rt.callback_query(F.data.startswith('complete:'),
                   StateFilter(FSMStates.viewing_task, FSMStates.editing_tasks))
async def complete_task(clb: CallbackQuery,state: FSMContext,user_db: dict):
  
    completed_homework = user_db["homeworks"][clb]#англ:стр 15 номер 1:пн
    if dueday == '':
        dueday = None

    del user_db["homeworks"][completed_homework]

    homeworks = user_db["homeworks"]
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton]
    for homework in homeworks:
        print(keys(homework)[0])
        buttons.append(InlineKeyboardButton(text=
                                            f'{homework["subject"]} - {homework["task"]}',
                                            callback_data=keys(homework)[0]))
    kb_builder.row(*buttons,width=1)
    kb_builder.row(*homework_service_butts,width=1)
    await clb.message.edit_text(text='Задание выполнено!',
                                reply_markup=kb_builder.as_markup(
                                    resize_keyboard=True
                                ))
    logging.debug(f'User {clb.from_user.full_name} has successfully completed task: {completed_homework}\n')
    await state.set_state(FSMStates.editing_tasks)