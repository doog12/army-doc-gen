import asyncio
from io import BytesIO

import aiohttp
from aiogram import Bot
from aiogram.types import BufferedInputFile


async def download_and_send_file(
    bot: Bot, docx_url: str, subtype_name: str, chat_id: int, callback_function
):
    status_msg = await bot.send_message(chat_id=chat_id, text="📥 Завантаження файлу...")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(docx_url, timeout=30) as response:
                if response.status == 200:
                    file_bytes = await response.read()
                    file = BytesIO(file_bytes)
                    file_name = f"{subtype_name}.docx"

                    # Wrap the BytesIO object in an InputFile
                    input_file = BufferedInputFile(file_bytes, filename=file_name)

                    await bot.send_document(chat_id=chat_id, document=input_file)
                    await bot.delete_message(chat_id=chat_id, message_id=status_msg.message_id)
                    await bot.send_message(chat_id=chat_id, text="✅ Файл успішно завантажено")
                    await bot.send_message(
                        chat_id=chat_id,
                        text="📁 Оберіть тип документа (крок 1 з 3):",
                        reply_markup=callback_function(),
                    )
                else:
                    await bot.send_message(
                        chat_id=chat_id, text="❌ Помилка при завантаженні DOCX."
                    )
    except asyncio.TimeoutError:
        await bot.send_message(chat_id=chat_id, text="⏱️ Тайм-аут при завантаженні файлу.")
    except Exception as e:
        await bot.send_message(chat_id=chat_id, text=f"❌ Сталася помилка: {str(e)}")
