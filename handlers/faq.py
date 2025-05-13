from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from configs.faqText import faq_text

router = Router()


@router.message(Command("faq"))
async def send_faq(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⚙️ Допомога", callback_data="help")],
            [InlineKeyboardButton(text="🔙 В головне меню", callback_data="back_to_start")],
        ]
    )
    await message.answer(
        faq_text, reply_markup=keyboard, parse_mode="Markdown", disable_web_page_preview=True
    )
