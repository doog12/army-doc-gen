from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_type_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📄 Рапорт", callback_data="doc_type:рапорт"),
                InlineKeyboardButton(text="📝 Заява", callback_data="civil_statement:заява"),
            ],
            [
                InlineKeyboardButton(text="ℹ️ FAQ / Інструкція", callback_data="faq"),
                InlineKeyboardButton(text="⚙️ Допомога", callback_data="help"),
            ],
            [InlineKeyboardButton(text="🌐 СЕД НГУ", callback_data="sed")],
        ]
    )
