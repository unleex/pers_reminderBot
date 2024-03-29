import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import logging
logger = logging.getLogger(__name__)


from aiogram.types import Message,CallbackQuery
from aiogram.filters import Command, CommandStart,StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram import Router, F

from lexicon.lexicon import LEXICON_RU
from states.states import FSMStates
from services.services import edit_user_db
from keyboards.schedule_days_keyboards import viewdays_kb_builder, menu_keyboard

from datetime import datetime
import json

rt = Router()

@rt.message(CommandStart())
async def info_start_command(message: Message,state: FSMContext,user_db: dict):
    await message.answer(text=LEXICON_RU['start_command_text'])
    user_data = message.from_user
    if not str(user_data.id) in json.load(open('db/db.json','r')):
        user_db = {
                "homeworks": {},
                "schedule": {'Понедельник': [], 
                              'Вторник': [], 
                              'Среда': [], 
                              'Четверг': [], 
                              'Пятница': [], 
                              'Суббота': [], 
                              'Воскресенье': []}
            }        
        edit_user_db(user_data.id,user_db)
        await message.answer(text=(LEXICON_RU['new_user_registered']
                                   .replace('name',message.from_user.full_name)))
        logger.info(f'New user registered. \n'
                    f'Name: {user_data.first_name} {user_data.last_name}.\n' 
                    f'ID: {user_data.id}')
    await state.clear()


@rt.message(Command(commands='help'))
async def info_help_command(message: Message):
    await message.answer(text=LEXICON_RU['info_command_text'])


@rt.callback_query(F.data=='return_to_viewdays',StateFilter(default_state))
async def return_to_viewdays(clb: CallbackQuery):
    await clb.message.edit_text(text=("Выбери день, расписание которого "
                                      "хочешь посмотреть."),
                                      reply_markup=viewdays_kb_builder.as_markup(resize_keyboard=True)
                                      )

#back to menu
@rt.callback_query(F.data=='return_to_menu',StateFilter(FSMStates.editing_tasks,FSMStates.viewing_schedule, 
                                                        FSMStates.viewing_day,FSMStates.editing_schedule))
async def return_to_menu(clb: CallbackQuery,state: FSMContext,user_db: dict):
    days_en_ru = {'Mon':"Понедельник",
                 'Tue':"Вторник",
                 'Wed':"Среда",
                 'Thu':"Четверг",
                 'Fri':"Пятница",
                 'Sat':"Суббота",
                 'Sun':"Воскресенье"}
    
    weekday = datetime.today().strftime('%a')
    schedule = user_db['schedule'][days_en_ru[weekday]]
    schedule_text = ''
    j = 1
    for i in schedule:
        schedule_text += f'{j}. {i.capitalize()}\n'
        j += 1
    await clb.message.edit_text(text=f"Расписание на сегодня:\n {schedule_text}",
                     reply_markup=menu_keyboard)
    await state.clear()
#main
@rt.message(Command(commands='menu'))
async def call_menu_command(msg: Message,state: FSMContext,user_db: dict):
    days_en_ru = {'Mon':"Понедельник",
                 'Tue':"Вторник",
                 'Wed':"Среда",
                 'Thu':"Четверг",
                 'Fri':"Пятница",
                 'Sat':"Суббота",
                 'Sun':"Воскресенье"}
    
    weekday = datetime.today().strftime('%a')
    schedule = user_db['schedule'][days_en_ru[weekday]]
    schedule_text = ''
    j = 1
    for i in schedule:
        schedule_text += f'{j}. {i.capitalize()}\n'
        j += 1
    await msg.answer(text=f"Расписание на сегодня:\n {schedule_text}",
                     reply_markup=menu_keyboard)
    await state.clear()


@rt.message()
async def else_handler(msg: Message):
    await msg.answer(LEXICON_RU['UnknownInstruction'])
    logger.info(f'Unknown instruction: {msg.text}, by {msg.from_user.id}')