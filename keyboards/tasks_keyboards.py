from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from my_typing.typing import schedule
from my_typing.typing import Homework
from services.services import gen_tasks_inline_kb
from my_typing.typing import schedule

homework_kb_builder = InlineKeyboardBuilder()
task_butts = gen_tasks_inline_kb(schedule.tasks)
homework_kb_builder.row(*task_butts,width=1)
edit = InlineKeyboardButton(
    text='✅Отметить выполненными',
    callback_data='enable_completing_tasks'
)
to_menu = InlineKeyboardButton(
   text = '⬅️В меню',
   callback_data='return_to_menu'
)
homework_kb_builder.row(edit,to_menu,width=1)

confirm = InlineKeyboardButton(text='✅Добавить',callback_data='confirm_add_task')
cancel = InlineKeyboardButton(text='❌Отмена',callback_data='cancel_add_task')
adding_task_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [confirm],
        [cancel]
    ],resize_keyboard=True
)