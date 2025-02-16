import logging
import aiohttp
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession
from config import BOT_TOKEN, API_URL

# Налаштовуємо логування
logging.basicConfig(level=logging.INFO)

# Ініціалізуємо сесію та бота
session = AiohttpSession()
bot = Bot(token=BOT_TOKEN, session=session)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer("Привіт! Надішли мені фото, і я його класифікую 🚀")

@dp.message(lambda msg: msg.photo, flags={"content_types": ContentType.PHOTO})
async def handle_photo(message: types.Message):
    photo = message.photo[-1]  # Беремо найбільше фото
    file_info = await bot.get_file(photo.file_id)
    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"

    # Завантажуємо фото і надсилаємо його FastAPI
    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as resp:
            image_data = await resp.read()

        form = aiohttp.FormData()
        form.add_field("file", image_data, filename="image.jpg", content_type="image/jpeg")

        async with session.post(API_URL, data=form) as resp:
            result = await resp.json()

    prediction = result.get("prediction", "❌ Помилка")
    confidence = result.get("confidence", "?")

    await message.answer(f"✅ Результат: {prediction} ({confidence})")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
