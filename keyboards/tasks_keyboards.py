from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from my_typing.typing import schedule
from my_typing.typing import schedule

homework_kb_builder = InlineKeyboardBuilder()#
edit = InlineKeyboardButton(
    text='✅Отметить выполненными',
    callback_data='enable_completing_tasks'
)
to_menu = InlineKeyboardButton(
   text = '⬅️В меню',
   callback_data='return_to_menu'
)
homework_service_butts = [edit,to_menu]

confirm = InlineKeyboardButton(
    text='✅Добавить',
    callback_data='confirm_add_task')

cancel = InlineKeyboardButton(
    text='❌Отмена',
    callback_data='cancel_add_task')

adding_task_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [confirm],
        [cancel]
    ],resize_keyboard=True
)