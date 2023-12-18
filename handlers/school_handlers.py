import sys
import os
from pprint import pprint


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup,CallbackQuery
from aiogram.filters import Command
from aiogram import Router, F
rt = Router()
from states.states import editing_schedule

from keyboards.keyboards import call_schedule_keyboard
@rt.message(F.text.lower().in_(["расписание","сегодня", "завтра"]))
async def call_schedule_command(msg: Message):
    editing_schedule=True
    await msg.answer(text='*here will be schedule on today or tomorrow*',
                     reply_markup=call_schedule_keyboard)

@rt.callback_query(F.data=='edit_schedule')
async def edit_schedule_command(clb: CallbackQuery):
    await clb.message.answer('callback successfully handled')

class Schedule:
    week_schedule={}

schedule = Schedule()