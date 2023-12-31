import sys
import os


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from aiogram.types import CallbackQuery
from lexicon.lexicon import LEXICON_RU
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router, F
from keyboards.tasks_keyboards import homework_kb_builder
rt = Router()

days = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']
editdays = [f'edit{i}' for i in days]
viewdays = [f'view{i}' for i in days]
    


#tasks
@rt.callback_query(F.data=='edit_tasks',StateFilter(default_state))
async def tasks_menu(clb: CallbackQuery):
    await clb.message.answer(text=LEXICON_RU['edit_tasks_text'],
                             reply_markup=homework_kb_builder.as_markup(resize_keyboard=True))