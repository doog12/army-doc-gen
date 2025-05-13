from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart

from keyboards.inline import get_main_type_keyboard
import os
from dotenv import load_dotenv

router = Router()


class AuthForm(StatesGroup):
    password = State()


load_dotenv()
AUTH_PASSWORD = os.getenv("BOT_PASSWORD")


@router.message(CommandStart())
async def ask_password(message: Message, state: FSMContext):
    await state.set_state(AuthForm.password)
    msg = await message.answer("🔐 Введіть пароль для доступу до бота:")
    await state.update_data(prompt_msg_id=msg.message_id)


@router.message(AuthForm.password)
async def verify_password(message: Message, state: FSMContext):
    fullUserName = message.from_user.full_name
    userName = f" (@{message.from_user.username})" if message.from_user.username else ""
    user_data = await state.get_data()
    prompt_msg_id = user_data.get("prompt_msg_id")

    if message.text.strip() == AUTH_PASSWORD:
        await state.clear()

        await message.delete()

        # Удалить сообщение бота "🔐 Введіть пароль..."
        if prompt_msg_id:
            try:
                await message.bot.delete_message(chat_id=message.chat.id, message_id=prompt_msg_id)
            except:
                pass  # сообщение могло быть уже удалено
        await message.answer("✅ Авторизація успішна!\n\n")
        await message.answer(
            f"👋 Привіт, {fullUserName}{userName}! Я бот для генерації документів.\n\n"
            "📁 Оберіть тип документа (крок 1 з 3):",
            reply_markup=get_main_type_keyboard(),
        )
    else:
        await message.answer("❌ Невірний пароль. Спробуйте ще раз:")
