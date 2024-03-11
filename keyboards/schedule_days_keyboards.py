from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
#schedule
butt_edit_schedule = InlineKeyboardButton(
    text='Изменить/создать расписание уроков',
    callback_data='edit_schedule'
)
butt_edit_tasks = InlineKeyboardButton(
    text='Домашние задания', 
    callback_data='edit_tasks'
)
butt_view_schedule = InlineKeyboardButton(
    text='Посмотреть расписание уроков',
    callback_data='view_schedule'
)

call_schedule_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[butt_edit_schedule],
                      [butt_edit_tasks],
                      [butt_view_schedule]]
)
#   edit schedule
days = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']
editdays = [f'edit{i}' for i in days]
editdays_butts = [InlineKeyboardButton(
    text=days[i], 
    callback_data=editdays[i]) for i in range(7)]
confirm = InlineKeyboardButton(
    text='✅Создать',
    callback_data='confirm_edit_schedule')
cancel = InlineKeyboardButton(
    text='❌Отмена',
    callback_data='cancel_edit_schedule')
editdays_kb_builder = InlineKeyboardBuilder()
editdays_kb_builder.row(*editdays_butts,width=1)
editdays_kb_builder.row(confirm,cancel,width=1)


#view schedule
days = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']
viewdays = [f'view{i}' for i in days]
viewdays_butts = [InlineKeyboardButton(text=days[i], 
                                       callback_data=viewdays[i]) for i in range(7)]
to_menu = InlineKeyboardButton(
    text='⬅️В меню', 
    callback_data='return_to_menu')
viewdays_kb_builder = InlineKeyboardBuilder()
viewdays_kb_builder.row(*viewdays_butts,width=1)
viewdays_kb_builder.row(to_menu)


#   view day
view_day_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(
        text='⬅️В дни',
        callback_data='return_to_viewdays'
    )]],resize_keyboard=True
)


#cancel day editing
cancel_edit_day_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(
        text='❌Отмена',
        callback_data='cancel_edit_day'
    )]]
)