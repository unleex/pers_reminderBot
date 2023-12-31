from aiogram.types import Message,CallbackQuery
from aiogram.filters import Command, CommandStart,StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from lexicon.lexicon import LEXICON_RU
from aiogram import Router, F
from states.states import FSMStates
from keyboards.schedule_days_keyboards import viewdays_kb_builder, call_schedule_keyboard
rt = Router()
@rt.message(CommandStart(), StateFilter(default_state))
async def info_start_command(message: Message):
    await message.answer(text=LEXICON_RU['start_command_text'])

@rt.message(Command(commands='help'),StateFilter(default_state))
async def info_help_command(message: Message):
    await message.answer(text=LEXICON_RU['info_command_text'])


@rt.callback_query(F.data=='return_to_viewdays',StateFilter(default_state))
async def return_to_viewdays(clb: CallbackQuery):
    await clb.message.edit_text(text=("Выбери день, расписание которого "
                                      "хочешь посмотреть."),
                                      reply_markup=viewdays_kb_builder.as_markup(resize_keyboard=True)
                                      )

#back to menu
@rt.callback_query(F.data=='return_to_menu',StateFilter(default_state))
async def return_to_menu(clb: CallbackQuery,state: FSMContext):
    await clb.message.edit_text(text='*here will be schedule on today or tomorrow*',
                     reply_markup=call_schedule_keyboard)
    await state.clear()
#main
@rt.message(Command(commands='schedule'),StateFilter(default_state))
async def call_schedule_command(msg: Message):
    await msg.answer(text='*here will be schedule on today or tomorrow*',
                     reply_markup=call_schedule_keyboard)