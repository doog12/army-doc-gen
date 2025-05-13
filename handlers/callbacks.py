from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from config import DOCUMENTS
from keyboards.inline import get_main_type_keyboard
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from modules.downloadFile import download_and_send_file
from configs.faqText import faq_text
from configs.helpText import help_text
from handlers.auth import AuthForm

router = Router()


# --- FSM состояния ---
class Form(StatesGroup):
    doc_type = State()
    authority = State()
    subtype = State()


@router.callback_query()
async def handle_callback(query: CallbackQuery, state: FSMContext):

    current_state = await state.get_state()
    if current_state == AuthForm.password:
        await query.answer("🔐 Спочатку введіть пароль.", show_alert=True)
        return

    data = query.data.split(":")
    await query.answer()

    # Назад к выбору типа документа
    if query.data == "back_to_start":
        await state.clear()
        await query.message.edit_text(
            "📁 Оберіть тип документа (крок 1 з 3):", reply_markup=get_main_type_keyboard()
        )
        return

    # Шаг 1 — выбор типа документа
    if data[0] == "doc_type":
        doc_type = data[1]
        await state.update_data(doc_type=doc_type)

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="👮 Командиру", callback_data="authority:командир")],
                [InlineKeyboardButton(text="📋 Начальнику", callback_data="authority:начальник")],
                [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_start")],
            ]
        )

        await query.message.edit_text(
            f"🔍 Обрано тип: *{doc_type.capitalize()}*\n\n👤 Оберіть отримувача (крок 2 з 3):",
            reply_markup=keyboard,
        )
        await state.set_state(Form.authority)
        return

    # Шаг 2 — выбор получателя (командиру или начальнику)
    if data[0] == "authority":
        authority = data[1]
        user_data = await state.get_data()
        doc_type = user_data.get("doc_type")
        if not doc_type:
            await query.message.answer("⚠️ Помилка. Почніть спочатку.")
            await state.clear()
            return

        await state.update_data(authority=authority)

        subtypes = DOCUMENTS.get(doc_type, {})
        keyboard = [
            [InlineKeyboardButton(text=doc["name"].capitalize(), callback_data=f"subtype:{key}")]
            for key, doc in subtypes.items()
        ]
        keyboard.append(
            [InlineKeyboardButton(text="🔙 Назад", callback_data=f"doc_type:{doc_type}")]
        )

        await query.message.edit_text(
            f"📤 Отримувач: *{authority.capitalize()}*\n\n📌 Оберіть підтип (крок 3 з 3):",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
        )
        await state.set_state(Form.subtype)
        return

    if query.data == "back_to_authority":
        user_data = await state.get_data()
        doc_type = user_data.get("doc_type")

        if not doc_type:
            await query.message.answer("⚠️ Помилка. Почніть спочатку.")
            await state.clear()
            return

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="👮 Командиру", callback_data="authority:командир")],
                [InlineKeyboardButton(text="📋 Начальнику", callback_data="authority:начальник")],
                [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_start")],
            ]
        )

        await query.message.edit_text(
            f"🔍 Обрано тип: *{doc_type.capitalize()}*\n\n👤 Оберіть отримувача (крок 2 з 3):",
            reply_markup=keyboard,
        )
        await state.set_state(Form.authority)
        return

    # Шаг 2/1 — выбор подтипа (для гражданского заявления)
    if data[0] == "civil_statement":
        doc_type = data[1]
        await state.update_data(doc_type=doc_type)
        if not doc_type:
            await query.message.answer("⚠️ Помилка. Почніть спочатку.")
            await state.clear()
            return

        subtypes = DOCUMENTS.get(doc_type, {})
        keyboard = [
            [InlineKeyboardButton(text=doc["name"].capitalize(), callback_data=f"subtype:{key}")]
            for key, doc in subtypes.items()
        ]
        keyboard.append([InlineKeyboardButton(text="🔙 Назад", callback_data=f"back_to_start")])

        await query.message.edit_text(
            f"📌 Оберіть підтип (2 з 2):",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
        )
        await state.set_state(Form.subtype)
        return

    # Шаг 3 — выбор подтипа
    if data[0] == "subtype":
        subtype_key = data[1]
        user_data = await state.get_data()
        doc_type = user_data.get("doc_type")
        authority = user_data.get("authority")

        doc = DOCUMENTS.get(doc_type, {}).get(subtype_key)
        if not doc:
            await query.message.answer("❌ Документ не знайдено.")
            return

        if doc_type == "заява":
            # Заява — без ролей
            docx_id = doc.get("docx")
            pdf_id = doc.get("pdf")
        else:
            # Рапорт — с ролями
            docx_id = (
                doc.get("docx_commander") if authority == "командир" else doc.get("docx_chief")
            )
            pdf_id = doc.get("pdf_commander") if authority == "командир" else doc.get("pdf_chief")

        if not docx_id or not pdf_id:
            await query.message.answer(
                "⚠️ Для цього підтипу не знайдені файли. Зверніться до адміністратора."
            )
            return

        pdf_url = f"https://drive.google.com/file/d/{pdf_id}/preview"

        # await state.update_data(authority=authority)
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📥 Завантажити", callback_data=f"download:{subtype_key}"
                    ),
                    InlineKeyboardButton(text="👁️ Переглянути", url=pdf_url),
                ],
                [InlineKeyboardButton(text="🔙 Назад", callback_data=f"back_to_authority")],
            ]
        )

        await query.message.edit_text(
            f"✅ Обрано: {doc_type.capitalize()} → {doc['name'].capitalize()}",
            reply_markup=keyboard,
        )
        return

    # Шаг 4 — загрузка файла
    if data[0] == "download":
        subtype_key = data[1]
        user_data = await state.get_data()
        doc_type = user_data.get("doc_type")
        authority = user_data.get("authority")

        doc = DOCUMENTS.get(doc_type, {}).get(subtype_key)
        if not doc:
            await query.message.answer("❌ Документ не знайдено.")
            return

        if doc_type == "заява":
            docx_id = doc.get("docx")
        else:
            docx_id = (
                doc.get("docx_commander") if authority == "командир" else doc.get("docx_chief")
            )

        if not docx_id:
            await query.message.answer("⚠️ DOCX файл не знайдено.")
            return

        docx_url = f"https://drive.google.com/uc?export=download&id={docx_id}"

        await download_and_send_file(
            query.bot,
            docx_url,
            doc["name"],
            query.message.chat.id,
            callback_function=get_main_type_keyboard,
        )
        await query.message.delete()

    # FAQ / Інструкція
    #####################################
    if data[0] == "faq":
        await query.message.edit_reply_markup(None)
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="⚙️ Допомога", callback_data="help")],
                [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_start")],
            ]
        )
        await query.message.edit_text(faq_text, reply_markup=keyboard)
        return

    # Допомога
    #####################################
    if data[0] == "help":
        await query.message.edit_reply_markup(None)
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_start")]]
        )
        await query.message.edit_text(
            help_text, reply_markup=keyboard, disable_web_page_preview=True
        )
        return

    # Система електронного документообігу НГУ
    #####################################
    if data[0] == "sed":

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📚 Інструкція", callback_data="sed_intruction")],
                [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_start")],
            ]
        )
        await query.message.edit_text(
            "📚 Посібник для Системи Електронного Документообігу Національної гвардії України (СЕД НГУ)\n\n"
            "👇 Оберіть дію:",
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )
        return

    # Інструкція СЕД НГУ
    if data[0] == "sed_intruction":
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="sed")]]
        )
        await query.message.edit_text(
            "📚 Інструкція для Системи Електронного Документообігу Національної гвардії України (СЕД НГУ)\n\n"
            "👇 Завантажте інструкцію або перегляньте онлайн",
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )

        doc = DOCUMENTS.get("sed", {}).get("instruction")
        if not doc:
            await query.message.answer("❌ Документ не знайдено.")
            return

        pdf_id = doc.get("pdf")

        if not pdf_id:
            await query.message.answer("⚠️ Файли не знайдені. Зверніться до адміністратора.")
            return

        pdf_url = f"https://drive.google.com/file/d/{pdf_id}/preview"

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📥 Завантажити", callback_data=f"download_sed:{pdf_id}"
                    ),
                    InlineKeyboardButton(text="👁️ Переглянути", url=pdf_url),
                ],
                [InlineKeyboardButton(text="🔙 Назад", callback_data=f"sed")],
            ]
        )

        await query.message.edit_text(
            "📚 Інструкція з користування СЕД НГУ\n\n"
            "👇 Завантажте інструкцію або перегляньте онлайн",
            reply_markup=keyboard,
        )
        return

    # Завантаження інструкції СЕД НГУ
    if data[0] == "download_sed":
        pdf_id = data[1]
        if not pdf_id:
            await query.message.answer("❌ Документ не знайдено.")
            return

        pdf_url = f"https://drive.google.com/uc?export=download&id={pdf_id}"

        await download_and_send_file(
            query.bot,
            pdf_url,
            "Інструкція СЕД НГУ",
            query.message.chat.id,
            callback_function=get_main_type_keyboard,
        )
        await query.message.delete()
