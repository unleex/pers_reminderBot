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
days = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']
mon = InlineKeyboardButton(text=days[0],callback_data=days[0])
tue = InlineKeyboardButton(text=days[1],callback_data=days[1])
wed = InlineKeyboardButton(text=days[2],callback_data=days[2])
thu = InlineKeyboardButton(text=days[3],callback_data=days[3])
fri = InlineKeyboardButton(text=days[4],callback_data=days[4])
sat = InlineKeyboardButton(text=days[5],callback_data=days[5])
sun = InlineKeyboardButton(text=days[6],callback_data=days[6])
confirm = InlineKeyboardButton(text='✅Создать',callback_data='confirm_edit_schedule')
cancel = InlineKeyboardButton(text=' ❌Отмена',callback_data='cancel_edit_schedule')
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