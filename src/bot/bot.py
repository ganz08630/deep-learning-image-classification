import logging
import aiohttp
import asyncio
import sys
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession
from config import BOT_TOKEN, API_URL

# Додаємо кореневу папку в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.database.database import save_prediction  # Тепер імпорт має працювати

# Налаштовуємо логування
logging.basicConfig(level=logging.INFO)

# Ініціалізуємо сесію та бота
session = AiohttpSession()
bot = Bot(token=BOT_TOKEN, session=session)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer("Привіт! Надішли мені фото, і я його класифікую 🚀")

async def fetch_prediction(file_url: str):
    """Відправляє зображення на FastAPI і отримує відповідь"""
    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as resp:
            image_data = await resp.read()

        form = aiohttp.FormData()
        form.add_field("file", image_data, filename="image.jpg", content_type="image/jpeg")

        async with session.post(API_URL, data=form) as resp:
            return await resp.json()

@dp.message(lambda msg: msg.photo, flags={"content_types": ContentType.PHOTO})
async def handle_photo(message: types.Message):
    photo = message.photo[-1]  # Беремо найбільше фото
    file_info = await bot.get_file(photo.file_id)
    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"

    # Отримуємо результат класифікації
    result = await fetch_prediction(file_url)
    prediction = result.get("prediction", "❌ Помилка")
    confidence = result.get("confidence", "?")

    try:
        confidence_value = float(confidence.replace("%", ""))  # Прибираємо '%' і перетворюємо у float
    except ValueError:
        confidence_value = 0.0  # Якщо раптом помилка, ставимо 0.0 (щоб не падало)

    # Зберігаємо в БД
    save_prediction(
        user_id=message.from_user.id,
        username=message.from_user.username,
        file_path=file_url,
        prediction=prediction,
        confidence=confidence_value
    )

    await message.answer(f"✅ Результат: {prediction} ({confidence_value}%)")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
