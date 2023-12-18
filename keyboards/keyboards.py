from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
butt_edit_schedule = InlineKeyboardButton(
    text='Изменить/создать расписание',
    callback_data='edit_schedule'
)
butt_edit_tasks = InlineKeyboardButton(
    text='Изменить домашние задания', 
    callback_data='edit_tasks'
)
call_schedule_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[butt_edit_schedule],
                      [butt_edit_tasks]]
)