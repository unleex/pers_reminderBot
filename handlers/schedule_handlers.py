import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from aiogram.types import CallbackQuery
from aiogram import Router, F
rt = Router()
from states.states import editing_schedule
from keyboards.keyboards import call_schedule_keyboard, edit_schedule_keyboard, view_schedule_keyboard,view_day_keyboard
from services.services import format_list
from lexicon.lexicon import LEXICON_RU
from states.states import schedule

days = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']
editdays = [f'edit{i}' for i in days]
viewdays = [f'view{i}' for i in days]

#   edit schedule
@rt.callback_query(F.data=='edit_schedule')
async def edit_schedule_command(clb: CallbackQuery):
    await clb.message.edit_text(text=(LEXICON_RU['edit_schedule_text']),
                                reply_markup=edit_schedule_keyboard)


#           confirm schedule editing
@rt.callback_query(F.data=='confirm_edit_schedule')
async def edit_schedule_confirm(clb: CallbackQuery):
    schedule.week_schedule.update(schedule.new_schedule)
    await clb.message.edit_text(
        text='Расписание заполнено!',
        reply_markup=call_schedule_keyboard
    )

#   cancel editing schedule
@rt.callback_query(F.data=='cancel_edit_schedule')
async def edit_schedule_cancel(clb: CallbackQuery):
    global editing_schedule
    editing_schedule = False
    schedule.new_schedule.clear()
    await clb.message.edit_text(
        text='Изменения отменены.',
        reply_markup=call_schedule_keyboard
    )
                               

#   view schedule
@rt.callback_query(F.data=='view_schedule')
async def view_schedule_command(clb: CallbackQuery):
    await clb.message.edit_text(text=("Выбери день, расписание которого "
                                      "хочешь посмотреть."),
                                      reply_markup=view_schedule_keyboard
                                      )


#       view day
@rt.callback_query(F.data.in_(viewdays))
async def view_day_command(clb: CallbackQuery):
    day = clb.data[4:]
    output = format_list(schedule.week_schedule[day])
    await clb.message.edit_text(text=output,
                                reply_markup=view_day_keyboard)
    