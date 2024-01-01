import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from my_typing.typing import schedule
to_menu = InlineKeyboardButton(text='⬅️В меню', callback_data='return_to_menu')
homework_kb_builder = InlineKeyboardBuilder()

homework_kb_builder.row(to_menu)
confirm = InlineKeyboardButton(
    text='✅Подтвердить',
    callback_data='confirm_add_task'
)
cancel = InlineKeyboardButton(
    text='❌Отмена',
    callback_data='cancel_add_task'
)
add_task_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [confirm],
        [cancel]]
)