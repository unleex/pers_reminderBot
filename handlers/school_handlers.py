import sys
import os
from pprint import pprint


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup,CallbackQuery
from aiogram.filters import Command
from aiogram import Router, F
rt = Router()
from states.states import editing_schedule
from keyboards.keyboards import call_schedule_keyboard, edit_schedule_keyboard, view_schedule_keyboard,view_day_keyboard,cancel_edit_day_keyboard
from services.services import statecheck, format_list

#schedule
#   call schedule
class Schedule:
    week_schedule={'Понедельник': ['Здесь пока пусто('],'Вторник':['Здесь пока пусто('],'Среда':['Здесь пока пусто('],'Четверг':['Здесь пока пусто('],'Пятница':['Здесь пока пусто('],'Суббота':['Здесь пока пусто('],'Воскресенье':['Здесь пока пусто(']}
    new_schedule={}
    clb: CallbackQuery
schedule = Schedule()
days = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']
editdays = [f'edit{i}' for i in days]
viewdays = [f'view{i}' for i in days]

#main
@rt.message(Command(commands='schedule'))
async def call_schedule_command(msg: Message):
    await msg.answer(text='*here will be schedule on today or tomorrow*',
                     reply_markup=call_schedule_keyboard)
    

#   edit schedule
@rt.callback_query(F.data=='edit_schedule')
async def edit_schedule_command(clb: CallbackQuery):
    await clb.message.edit_text(text=('Измени или создай расписание'
                                'уроков.\n'
                                '1. Нажми на кнопку дня, на который хочешь'
                                'заполнить/изменить расписание\n'
                                '2. Пришли уроки, <b>каждый–с новой строки,без номеров и других доп. символов</b>!\n'
                                '3. Когда закончишь, не забудь нажать ✅'
                                'Создать'),reply_markup=edit_schedule_keyboard)


#           edit day
@rt.callback_query(F.data.in_(editdays))
async def edit_day_command(clb: CallbackQuery):
    global editing_schedule
    editing_schedule=True
    await clb.message.edit_text(text='Присылай уроки, <b>каждый–с новой строки,'
                                'без номеров и других доп. символов</b>',
                                reply_markup=cancel_edit_day_keyboard)
    schedule.clb = clb


@statecheck
@rt.message()
async def edit_day_process(msg: Message,activate=editing_schedule):
    global editing_schedule
    schedule.new_schedule.update({schedule.clb.data[4:]: msg.text.split('\n')})
    output = format_list(schedule.new_schedule[schedule.clb.data[4:]])
    await schedule.clb.message.edit_text(
        text=(f'{schedule.clb.data[4:]}: расписание изменено!\n{output}'),
        reply_markup=edit_schedule_keyboard)#replace to adding a tick to inline button in editing schedule
    editing_schedule=False
    await msg.delete()


#       cancel day editing
@rt.callback_query(F.data=='cancel_edit_day')
async def cancel_edit_day(clb: CallbackQuery):
    global editing_schedule
    await clb.message.edit_text(text='Изменения отменены.',
                                reply_markup=edit_schedule_keyboard)
    
#           confirm schedule editing
@rt.callback_query(F.data=='confirm_edit_schedule')
async def edit_schedule_confirm(clb: CallbackQuery):
    schedule.week_schedule.update(schedule.new_schedule)
    await clb.message.edit_text(
        text='Расписание заполнено!',
        reply_markup=call_schedule_keyboard
    )

#   cancel editing schedule
@rt.callback_query(F.data=='cancel_edit_schedule')
async def edit_schedule_cancel(clb: CallbackQuery):
    global editing_schedule
    editing_schedule = False
    schedule.new_schedule.clear()
    await clb.message.edit_text(
        text='Изменения отменены.',
        reply_markup=call_schedule_keyboard
    )
                               

#   view schedule
@rt.callback_query(F.data=='view_schedule')
async def view_schedule_command(clb: CallbackQuery):
    await clb.message.edit_text(text=("Выбери день, расписание которого "
                                      "хочешь посмотреть."),
                                      reply_markup=view_schedule_keyboard
                                      )


#       view day
@rt.callback_query(F.data.in_(viewdays))
async def view_day_command(clb: CallbackQuery):
    day = clb.data[4:]
    output = format_list(schedule.week_schedule[day])
    await clb.message.edit_text(text=output,
                                reply_markup=view_day_keyboard)
    

@rt.callback_query(F.data=='return_to_viewdays')
async def return_to_viewdays(clb: CallbackQuery):
    await clb.message.edit_text(text=("Выбери день, расписание которого "
                                      "хочешь посмотреть."),
                                      reply_markup=view_schedule_keyboard
                                      )

#back to menu
@rt.callback_query(F.data=='return_to_menu')
async def return_to_menu(clb: CallbackQuery):
    await clb.message.edit_text(text='*here will be schedule on today or tomorrow*',
                     reply_markup=call_schedule_keyboard)