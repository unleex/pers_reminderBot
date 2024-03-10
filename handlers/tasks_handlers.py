import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery, Message, Message,InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram import Router, F

from datetime import datetime
from arq import ArqRedis

from lexicon.lexicon import LEXICON_RU
from keyboards.tasks_keyboards import homework_service_butts
from states.states import FSMStates
from services.services import (find_and_replace,
                               normalize_duedate,get_time_frommsg,get_day_frommsg,keys,edit_user_db)
from keyboards.tasks_keyboards import adding_task_kb
from states.states import FSMStates
from scheduler.alert_deadlines import schedule_deadline_alert
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
    buttons: list[InlineKeyboardButton] = []
    for key in homeworks:

        buttons.append(InlineKeyboardButton(text=
                                            f'{homeworks[key]["subject"]} - {homeworks[key]["task"]}',
                                            callback_data=f'view:{key}'))
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

    due_date = None
    if due_day:
        due_date = normalize_duedate(due_day)
        day_out = due_day
        out += f'Записано на {day_out}'

    homework_id = f'Homework_{msg.from_user.id}_{datetime.today().strftime("%Y/%m/%d_%H:%M:%S")}'
    await state.set_data(
        { 
        homework_id: {
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
async def confirm_adding_task(clb: CallbackQuery,state:FSMContext,arqredis: ArqRedis, user_db: dict):
    new_homework = await state.get_data()
    hw_data = list(new_homework.values())[0]

    due_datetime = None
    if hw_data["duedate"]:

        #add 2000 to year because it decreases to tens(2024->24)
        hw_data["duedate"][0] += 2000
        due_datetime = datetime(*hw_data["duedate"],*hw_data["duetime"])
        prealert_datetime = datetime(*hw_data["duedate"],hw_data["duetime"][0]-1, hw_data["duetime"][1])
        on_default_time_datetime = datetime(*hw_data["duedate"],*DEFAULT_DEADLINE_TIME)
        #alert on default_deadline_time, before hour of deadline and on deadline
        await schedule_deadline_alert(arqredis,clb.from_user.id,hw_data,due_datetime)
        await schedule_deadline_alert(arqredis,clb.from_user.id,hw_data,prealert_datetime)
        await schedule_deadline_alert(arqredis,clb.from_user.id,hw_data,on_default_time_datetime)

    user_db["homeworks"].update(new_homework)
    edit_user_db(clb.from_user.id, user_db)

    logger.info(msg=(f'New homework added.\n\t'
            f'User: {clb.from_user.id}\t'
            f'Subject: {hw_data["subject"]}\t' 
            f'Task: {hw_data["task"]}\t'
            f'Deadline: {due_datetime}'))
    await clb.message.edit_text('Задача добавлена!')
    await state.clear()


#cancel adding task
@rt.callback_query(F.data == 'cancel_add_task',StateFilter(FSMStates.adding_task))
async def cancel_add_task(clb: CallbackQuery,state:FSMContext,user_db: dict):

    del user_db["homeworks"]["Unconfirmed homework"]
    await clb.message.edit_text('Изменения отменены.')
    await state.clear()

#view task
@rt.callback_query(F.data.startswith('view:'),StateFilter(FSMStates.editing_tasks))
async def view_task_command(clb: CallbackQuery, state : FSMContext,user_db: dict):
    complete = InlineKeyboardButton(
        text='✅Выполнено',
        callback_data='complete:'+clb.data[5:]
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
        task = user_db["homeworks"][clb.data[5:]]
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

    del user_db["homeworks"][clb.data[9:]]
    edit_user_db(clb.from_user.id, user_db)
    homeworks = user_db["homeworks"]
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    for key in homeworks:
        buttons.append(InlineKeyboardButton(text=
                                            f'{homeworks[key]["subject"]} - {homeworks[key]["task"]}',
                                            callback_data='view:'+key))
    kb_builder.row(*buttons,width=1)
    kb_builder.row(*homework_service_butts,width=1)
    await clb.message.edit_text(text='Задание выполнено!',
                                reply_markup=kb_builder.as_markup(
                                    resize_keyboard=True
                                ))
    logging.debug(f'User {clb.from_user.id} has successfully completed task {clb.data[9:]}\n')
    await state.set_state(FSMStates.editing_tasks)