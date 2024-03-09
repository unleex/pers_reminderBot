from aiogram.types import BotCommand
from aiogram import Bot
async def set_main_menu(bot: Bot) -> None:
    main_menu_commands=[
        BotCommand(command='help', description='Информация о боте'),
        BotCommand(command='menu',description='Домашка/расписание'),
        BotCommand(command='start',description='Нажмите, eсли бот не отвечает')
    ]
    await bot.set_my_commands(main_menu_commands)