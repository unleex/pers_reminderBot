import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import logging
logger = logging.getLogger(__name__)

from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from aiogram import Router, F
from aiogram.fsm.state import default_state
from states.states import FSMStates
from aiogram.fsm.context import FSMContext

from keyboards.schedule_days_keyboards import menu_keyboard, editdays_kb_builder,viewdays_kb_builder
from services.services import edit_user_db
from lexicon.lexicon import LEXICON_RU

rt = Router()

days = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']
editdays = [f'edit{i}' for i in days]
viewdays = [f'view{i}' for i in days]


@rt.callback_query(F.data=='edit_schedule',StateFilter(default_state))
async def edit_schedule(clb: CallbackQuery, state: FSMContext):
    await clb.message.edit_text(text=(LEXICON_RU['edit_schedule_text']),
                                reply_markup=editdays_kb_builder.as_markup(resize_keyboard=True))
    await state.set_state(FSMStates.editing_schedule)  

#   view schedule
@rt.callback_query(F.data == 'view_schedule',StateFilter(default_state))
async def view_schedule(clb: CallbackQuery,state: FSMContext):
    await clb.message.edit_text(text=("Выбери день, расписание которого "
                                      "хочешь посмотреть."),
                                      reply_markup=viewdays_kb_builder.as_markup(resize_keyboard=True)
                                      )
    await state.set_state(FSMStates.viewing_schedule)


#       view day
@rt.callback_query(F.data.in_(viewdays),StateFilter(FSMStates.viewing_schedule, FSMStates.viewing_day))
async def view_day(clb: CallbackQuery, state: FSMContext,user_db: dict):
    j = 1
    output: str = ''
    for i in user_db["schedule"][clb.data[4:]]:
        output += f'{j}. {i.capitalize()}\n'
        j += 1

    if not output:
        output = f'{clb.data[4:]}: {LEXICON_RU["EmptySchedule"]}'
    await clb.message.edit_text(text=output,
                                reply_markup=viewdays_kb_builder.as_markup(resize_keyboard=True))
    await state.set_state(FSMStates.viewing_day)