import sys
import os
import datetime

# Додаємо кореневу папку в sys.path, щоб імпорти працювали коректно
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.bot.bot import fetch_prediction, send_welcome  # Тепер імпорт має працювати

import pytest
from aiogram import Dispatcher, types
#from src.bot.bot import fetch_prediction, send_welcome
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_fetch_prediction():
    """Тестуємо функцію fetch_prediction"""
    mock_response = {"prediction": "Cat", "confidence": "95%"}
    
    with patch("src.bot.bot.aiohttp.ClientSession.post") as mock_post:
        mock_post.return_value.__aenter__.return_value.json = AsyncMock(return_value=mock_response)

        result = await fetch_prediction("http://test-url.com/image.jpg")

        assert result == mock_response

@patch("aiogram.types.Message.answer", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_send_welcome(mock_answer):
    """Тестуємо команду /start"""
    dp = Dispatcher()
    message = types.Message(
        message_id=1,
        date=datetime.datetime.now(),
        chat=types.Chat(id=1, type="private"),
        text="/start"
    )

    # Викликаємо функцію, яка має відповісти на команду /start
    await send_welcome(message)

    # Перевіряємо, чи викликався answer()
    mock_answer.assert_called_once_with("Привіт! Я бот.")

