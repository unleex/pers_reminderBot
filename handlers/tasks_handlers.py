import sys
import os


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from aiogram.types import CallbackQuery
from aiogram import Router, F
rt = Router()

days = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']
editdays = [f'edit{i}' for i in days]
viewdays = [f'view{i}' for i in days]
    


#tasks
@rt.callback_query(F.data=='edit_tasks')
async def tasks_menu(clb: CallbackQuery):
    pass