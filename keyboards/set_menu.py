from aiogram.types import BotCommand
from aiogram import Bot
async def set_main_menu(bot: Bot) -> None:
    main_menu_commands=[
        BotCommand(command='help', description='Информация о боте'),
        BotCommand(command='schedule',description='Вызвать расписание')
    ]
    await bot.set_my_commands(main_menu_commands)