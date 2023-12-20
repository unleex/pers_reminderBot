import sys
import os
from pprint import pprint


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup,CallbackQuery
from aiogram.filters import Command
from aiogram import Router, F
rt = Router()
from states.states import editing_schedule
from keyboards.keyboards import call_schedule_keyboard, edit_schedule_keyboard


days = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']
new_day = {}
new_schedule = {}

@rt.message(Command(commands='schedule'))
async def call_schedule_command(msg: Message):
    editing_schedule=True
    await msg.answer(text='*here will be schedule on today or tomorrow*',
                     reply_markup=call_schedule_keyboard)

@rt.callback_query(F.data=='edit_schedule')
async def edit_schedule_command(clb: CallbackQuery):
    await clb.message.edit_text(text=('Измени или создай расписание'
                                'уроков.\n'
                                '1. Нажми на кнопку дня, на который хочешь'
                                'заполнить/изменить расписание\n'
                                '2. Пришли уроки, <b>каждый–с новой строки,без номеров и других доп. символов</b>!\n'
                                '3. Когда закончишь, не забудь нажать ✅'
                                'Создать'),reply_markup=edit_schedule_keyboard)

@rt.callback_query(F.data.in_(days))
async def edit_day_command(clb: CallbackQuery):
    await clb.message.edit_text(text='Присылай уроки, <b>каждый–с новой строки,'
                                'без номеров и других доп. символов</b>',
                                reply_markup=None)
    schedule.clb = clb


@rt.message()
async def add_day_process(msg: Message):
    schedule.new_schedule.update({schedule.clb.data: msg.text.split('\n')})
    output: str=''
    j = 1
    for i in schedule.new_schedule[schedule.clb.data]:
        output += f'{j}. {i.capitalize()}\n'
        j += 1
    await schedule.clb.message.edit_text(
        text=(f'{schedule.clb.data}: расписание изменено!\n{output}'),#make this edit the schedule msg
        reply_markup=edit_schedule_keyboard)#replace to adding a tick to inline button in editing schedule
class Schedule:
    week_schedule={}
    new_schedule={}
    clb: CallbackQuery
schedule = Schedule()