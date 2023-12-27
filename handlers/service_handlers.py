from aiogram.types import Message,ReplyKeyboardMarkup,KeyboardButton,ReplyKeyboardRemove,CallbackQuery
from aiogram.filters import Command, CommandStart
from lexicon.lexicon import LEXICON_RU
from aiogram import Router, F
from keyboards.schedule_days_keyboards import viewdays_kb_builder, call_schedule_keyboard
rt = Router()
@rt.message(CommandStart())
async def info_start_command(message: Message):
    await message.answer(text=LEXICON_RU['start_command_text'])

@rt.message(Command(commands='help'))
async def info_help_command(message: Message):
    await message.answer(text=LEXICON_RU['info_command_text'])


@rt.callback_query(F.data=='return_to_viewdays')
async def return_to_viewdays(clb: CallbackQuery):
    await clb.message.edit_text(text=("Выбери день, расписание которого "
                                      "хочешь посмотреть."),
                                      reply_markup=viewdays_kb_builder.as_markup(resize_keyboard=True)
                                      )

#back to menu
@rt.callback_query(F.data=='return_to_menu')
async def return_to_menu(clb: CallbackQuery):
    await clb.message.edit_text(text='*here will be schedule on today or tomorrow*',
                     reply_markup=call_schedule_keyboard)

#main
@rt.message(Command(commands='schedule'))
async def call_schedule_command(msg: Message):
    await msg.answer(text='*here will be schedule on today or tomorrow*',
                     reply_markup=call_schedule_keyboard)