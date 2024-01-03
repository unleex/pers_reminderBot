import sys
import os


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.filters import StateFilter
rt = Router()
from states.states import FSMStates
from keyboards.schedule_days_keyboards import editdays_kb_builder,cancel_edit_day_keyboard
from services.services import format_list
from lexicon.lexicon import LEXICON_RU
from my_typing.typing import schedule

days = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']
editdays = [f'edit{i}' for i in days]
viewdays = [f'view{i}' for i in days]

#           edit day
@rt.callback_query(F.data.in_(editdays),StateFilter(FSMStates.editing_schedule))
async def edit_day_command(clb: CallbackQuery,state: FSMContext):
    await clb.message.edit_text(text=LEXICON_RU['edit_days_text'],
                                reply_markup=cancel_edit_day_keyboard)
    schedule.clb = clb
    await state.set_state(FSMStates.editing_day)


@rt.message(StateFilter(FSMStates.editing_day))
async def edit_day_process(msg: Message,state: FSMContext):
    schedule.new_schedule.update({schedule.clb.data[4:]: msg.text.split('\n')})
    output = format_list(schedule.new_schedule[schedule.clb.data[4:]])
    await schedule.clb.message.edit_text(
        text=(f'{schedule.clb.data[4:]}: расписание изменено!\n{output}'),
        reply_markup=editdays_kb_builder.as_markup(resize_keyboard=True))#replace to adding a tick to inline button in editing schedule
    await msg.delete()
    await state.set_state(FSMStates.editing_schedule)


#       cancel day editing
@rt.callback_query(F.data=='cancel_edit_day',StateFilter(FSMStates.editing_day))
async def cancel_edit_day(clb: CallbackQuery,state: FSMContext):
    await clb.message.edit_text(text='Изменения отменены.',
                                reply_markup=editdays_kb_builder.as_markup(resize_keyboard=True))
    await state.set_state(FSMStates.editing_schedule)