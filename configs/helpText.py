import os
from dotenv import load_dotenv

load_dotenv()
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
CHIEF_NUMBER = os.getenv("CHIEF_NUMBER")

help_text = (
    "ℹ️ *Допомога користувачу:*\n\n"
    "⚙️ *Основні команди:*\n"
    "• /start — почати роботу з ботом.\n"
    "• /faq — інструкція користування.\n"
    "• /help — перегляд довідки та контактів.\n\n"

    "📌 *Що робити, якщо виникли труднощі?*\n"
    "• Натисніть кнопку *FAQ / Інструкція* в головному меню.\n"
    "• Зв’яжіться з адміністрацією за контактами нижче.\n\n"
    
    "📨 *Контакти підтримки:*\n"
    f"• 👤 [Адміністратор](https://t.me/{ADMIN_USERNAME})\n"
    f"• 👤 [Начальник](https://wa.me/{CHIEF_NUMBER})\n"
)