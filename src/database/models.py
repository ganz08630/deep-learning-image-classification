from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base  # новий варіант

import datetime
import os

# Визначаємо шлях до БД
DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Ініціалізуємо підключення до БД
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()

# Оголошуємо модель таблиці `predictions`
class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    username = Column(String, nullable=True)
    file_path = Column(String, nullable=False)
    prediction = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
