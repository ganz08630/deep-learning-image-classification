# Використовуємо Python 3.9.6
FROM python:3.9.6

# Встановлюємо робочу директорію всередині контейнера
WORKDIR /app

# Встановлюємо необхідні бібліотеки
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*  # Видаляємо кеш для зменшення розміру контейнера


# Копіюємо необхідні файли
COPY requirements.txt .
#COPY setup.py .
COPY src ./src
COPY models ./models
COPY src/frontend ./src/frontend 

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Додаємо шлях до Python-модулів
ENV PYTHONPATH="/app"

# Вказуємо стандартну команду для запуску API
CMD ["uvicorn", "src.api.server:app", "--host", "0.0.0.0", "--port", "8000"]

