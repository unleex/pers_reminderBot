import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import logging
logger = logging.getLogger(__name__)

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.filters import StateFilter

from states.states import FSMStates
from keyboards.schedule_days_keyboards import editdays_kb_builder,cancel_edit_day_keyboard
from lexicon.lexicon import LEXICON_RU
from filters.filters import IsDayScheduleFormat
from services.services import edit_user_db

rt = Router()
edit_day_clb = CallbackQuery

days = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']
editdays = [f'edit{i}' for i in days]
viewdays = [f'view{i}' for i in days]
#           edit day
@rt.callback_query(F.data.in_(editdays),StateFilter(FSMStates.editing_schedule))
async def edit_day_command(clb: CallbackQuery,state: FSMContext):
    global edit_day_clb#change to something neat
    edit_day_clb = clb

    await clb.message.edit_text(text=LEXICON_RU['edit_days_text'].replace('day', clb.data[4:]),
                                reply_markup=cancel_edit_day_keyboard)
    await state.set_data({'day': clb.data[4:]})
    await state.set_state(FSMStates.editing_day)


@rt.message(IsDayScheduleFormat(),StateFilter(FSMStates.editing_day, F.data.in_(editdays)))
async def edit_day_process(msg: Message, state: FSMContext, user_db: dict):
    global edit_day_clb 
    ctx_data = await state.get_data()
    output: str = ''
    j = 1
    for i in msg.text.split('\n'):
        output += f'{j}. {i.capitalize()}\n'
        j += 1
    await edit_day_clb.message.edit_text(
       text=(f'{ctx_data["day"]}: расписание изменено!\n{output}'),
       reply_markup=editdays_kb_builder.as_markup(resize_keyboard=True))
    await msg.delete()  
    user_db["schedule"][ctx_data["day"]] = msg.text.split('\n')
    edit_user_db(msg.from_user.id, user_db)
    await state.set_state(FSMStates.editing_schedule)
    logger.info(f'Schedule on {ctx_data["day"]} filled by {msg.from_user.id}')

#       cancel day editing
@rt.callback_query(F.data=='cancel_edit_day',StateFilter(FSMStates.editing_day))
async def cancel_edit_day(clb: CallbackQuery,state: FSMContext):
    await clb.message.edit_text(text='Изменения отменены.',
                                reply_markup=editdays_kb_builder.as_markup(resize_keyboard=True))
    await state.set_state(FSMStates.editing_schedule)