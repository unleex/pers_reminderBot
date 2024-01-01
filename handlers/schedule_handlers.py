import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from aiogram import Router, F
rt = Router()
from aiogram.fsm.state import default_state
from states.states import FSMStates
from aiogram.fsm.context import FSMContext
from keyboards.schedule_days_keyboards import call_schedule_keyboard, editdays_kb_builder,viewdays_kb_builder
from services.services import format_list
from lexicon.lexicon import LEXICON_RU
from my_typing.typing import schedule

days = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']
editdays = [f'edit{i}' for i in days]
viewdays = [f'view{i}' for i in days]

#   edit schedule
@rt.callback_query(F.data=='edit_schedule',StateFilter(default_state))
async def edit_schedule_command(clb: CallbackQuery, state: FSMContext):
    await clb.message.edit_text(text=(LEXICON_RU['edit_schedule_text']),
                                reply_markup=editdays_kb_builder.as_markup(resize_keyboard=True))
    await state.set_state(FSMStates.editing_schedule)
    


#           confirm schedule editing
@rt.callback_query(F.data=='confirm_edit_schedule',StateFilter(FSMStates.editing_schedule))
async def edit_schedule_confirm(clb: CallbackQuery,state: FSMContext):
    schedule.week_schedule.update(schedule.new_schedule)
    await clb.message.edit_text(
        text='Расписание заполнено!',
        reply_markup=call_schedule_keyboard
    )
    await state.clear()

#   cancel editing schedule
@rt.callback_query(F.data=='cancel_edit_schedule',StateFilter(FSMStates.editing_schedule))
async def edit_schedule_cancel(clb: CallbackQuery, state: FSMContext):
    schedule.new_schedule.clear()
    await clb.message.edit_text(
        text='Изменения отменены.',
        reply_markup=call_schedule_keyboard
    )
    await state.clear()
                               

#   view schedule
@rt.callback_query(F.data=='view_schedule')
async def view_schedule_command(clb: CallbackQuery):
    await clb.message.edit_text(text=("Выбери день, расписание которого "
                                      "хочешь посмотреть."),
                                      reply_markup=viewdays_kb_builder.as_markup(resize_keyboard=True)
                                      )


#       view day
@rt.callback_query(F.data.in_(viewdays))
async def view_day_command(clb: CallbackQuery):
    day = clb.data[4:]
    output = format_list(schedule.week_schedule[day])
    await clb.message.edit_text(text=output,
                                reply_markup=viewdays_kb_builder.as_markup(resize_keyboard=True))