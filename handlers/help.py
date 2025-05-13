from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from configs.helpText import help_text

router = Router()

# Обработчик команды /help
@router.message(Command("help"))
async def send_help(message: Message):    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[    
    [InlineKeyboardButton(text="🔙 В головне меню", callback_data="back_to_start")]
    ])
    await message.answer(
        help_text,
        reply_markup=keyboard,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )