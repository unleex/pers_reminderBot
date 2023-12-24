from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
#schedule
butt_edit_schedule = InlineKeyboardButton(
    text='Изменить/создать расписание',
    callback_data='edit_schedule'
)
butt_edit_tasks = InlineKeyboardButton(
    text='Домашние задания', 
    callback_data='edit_tasks'
)
butt_view_schedule = InlineKeyboardButton(
    text='Посмотреть полное расписание',
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
mon = InlineKeyboardButton(text=days[0],callback_data=editdays[0])
tue = InlineKeyboardButton(text=days[1],callback_data=editdays[1])
wed = InlineKeyboardButton(text=days[2],callback_data=editdays[2])
thu = InlineKeyboardButton(text=days[3],callback_data=editdays[3])
fri = InlineKeyboardButton(text=days[4],callback_data=editdays[4])
sat = InlineKeyboardButton(text=days[5],callback_data=editdays[5])
sun = InlineKeyboardButton(text=days[6],callback_data=editdays[6])
confirm = InlineKeyboardButton(text='✅Создать',callback_data='confirm_edit_schedule')
cancel = InlineKeyboardButton(text='❌Отмена',callback_data='cancel_edit_schedule')
edit_schedule_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[mon],
                     [tue],
                     [wed],
                     [thu],
                     [fri],
                     [sat],
                     [sun],
                     [confirm],
                     [cancel]]
)
#view schedule
viewdays = [f'view{i}' for i in days]
mon = InlineKeyboardButton(text=days[0],callback_data=viewdays[0])
tue = InlineKeyboardButton(text=days[1],callback_data=viewdays[1])
wed = InlineKeyboardButton(text=days[2],callback_data=viewdays[2])
thu = InlineKeyboardButton(text=days[3],callback_data=viewdays[3])
fri = InlineKeyboardButton(text=days[4],callback_data=viewdays[4])
sat = InlineKeyboardButton(text=days[5],callback_data=viewdays[5])
sun = InlineKeyboardButton(text=days[6],callback_data=viewdays[6])
to_menu= InlineKeyboardButton(text=' ⬅️В меню',callback_data='return_to_menu')
view_schedule_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[mon],
                     [tue],
                     [wed],
                     [thu],
                     [fri],
                     [sat],
                     [sun],
                     [to_menu]]
)

#   view day
view_day_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(
        text='⬅️В дни',
        callback_data='return_to_viewdays'
    )]]
)
#cancel day editing
cancel_edit_day_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(
        text='❌Отмена',
        callback_data='cancel_edit_day'
    )]]
)