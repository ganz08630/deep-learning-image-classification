import os
from dotenv import load_dotenv

# Завантажуємо змінні середовища
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/predict/")  # FastAPI URL
