from aiogram.types import Message,ReplyKeyboardMarkup,KeyboardButton,ReplyKeyboardRemove
from aiogram.filters import Command, CommandStart

from aiogram import Router
rt = Router()
@rt.message(CommandStart())
async def info_start_command(message: Message):
    await message.answer(text='Привет! Это бот-напоминалка, с которым ты ничего не забудешь. Для ознакомления с функционалом отправь комманду /help')

@rt.message(Command(commands='help'))
async def info_help_command(message: Message):
    await message.answer(text='Привет! это бот для тайм-менеджмента! Ты можешь составить расписание уроков, если школьник,\n'
                         'или просто составить список дел на неделю или даже месяц!')