import sys
import os
from pprint import pprint


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup,CallbackQuery
from aiogram.filters import Command
from aiogram import Router, F
rt = Router()
from states.states import editing_schedule
from keyboards.keyboards import call_schedule_keyboard, edit_schedule_keyboard, view_schedule_keyboard,view_day_keyboard,cancel_edit_day_keyboard
from services.services import statecheck, format_list
from lexicon.lexicon import LEXICON_RU
from states.states import schedule

days = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']
editdays = [f'edit{i}' for i in days]
viewdays = [f'view{i}' for i in days]

#           edit day
@rt.callback_query(F.data.in_(editdays))
async def edit_day_command(clb: CallbackQuery):
    global editing_schedule
    editing_schedule=True
    await clb.message.edit_text(text=LEXICON_RU['edit_days_text'],
                                reply_markup=cancel_edit_day_keyboard)
    schedule.clb = clb


@statecheck
@rt.message()
async def edit_day_process(msg: Message,activate=editing_schedule):
    global editing_schedule
    schedule.new_schedule.update({schedule.clb.data[4:]: msg.text.split('\n')})
    output = format_list(schedule.new_schedule[schedule.clb.data[4:]])
    await schedule.clb.message.edit_text(
        text=(f'{schedule.clb.data[4:]}: расписание изменено!\n{output}'),
        reply_markup=edit_schedule_keyboard)#replace to adding a tick to inline button in editing schedule
    editing_schedule=False
    await msg.delete()


#       cancel day editing
@rt.callback_query(F.data=='cancel_edit_day')
async def cancel_edit_day(clb: CallbackQuery):
    global editing_schedule
    await clb.message.edit_text(text='Изменения отменены.',
                                reply_markup=edit_schedule_keyboard)