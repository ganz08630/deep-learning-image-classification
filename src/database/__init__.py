from .models import Base, engine

# Створюємо всі таблиці у базі (якщо їх ще немає)
Base.metadata.create_all(bind=engine)
