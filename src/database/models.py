from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime
import os

# Визначаємо шлях до БД
DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Підключаємо ORM
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовий клас для моделей
Base = declarative_base()

# Оголошуємо модель таблиці predictions
class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    username = Column(String, nullable=True)
    file_path = Column(String, nullable=False)
    prediction = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# Функція ініціалізації БД (не потрібна при використанні Alembic)
def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print(f"✅ База даних ініціалізована в {DB_PATH}")
