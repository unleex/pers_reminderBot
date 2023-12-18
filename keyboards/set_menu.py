from aiogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot
async def set_main_menu(bot: Bot) -> None:
    main_menu_commands=[
        BotCommand(command='help', description='Информация о боте'),
    ]
    await bot.set_my_commands(main_menu_commands)
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