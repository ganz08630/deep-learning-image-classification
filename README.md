📌 Deep Learning Image Classification

🔥 Опис проєкту

Цей проєкт створений для тестування повного циклу роботи з нейронною мережею, включаючи:

Створення нейромережі для класифікації зображень.

Розгортання нейромережі на сервері (бекенд на Python + FastAPI, запакований у Docker).

Розробку клієнтського застосунку (фронтенд на React + TailwindCSS), який взаємодіє із сервером через API.

📂 Структура проєкту

.
├── Dockerfile
├── docker-compose.yml
├── frontend/           # Фронтенд (React + TailwindCSS)
│   ├── src/           # Основний код React
│   ├── public/        # Публічні ресурси
│   ├── package.json   # Список залежностей
│   └── tailwind.config.js  # Конфігурація TailwindCSS
├── models/            # Файли моделей нейромережі
│   └── cifar10_model.h5
├── src/               # Бекенд (FastAPI, обробка запитів)
│   ├── api/           # API-сервер
│   ├── inference/     # Логіка передбачення
│   ├── training/      # Логіка навчання нейромережі
│   ├── dataset_loader.py  # Завантаження датасету
│   ├── config.py      # Налаштування
│   ├── utils/         # Додаткові утиліти
├── test_images/       # Тестові зображення
└── requirements.txt   # Залежності Python

🚀 Технології

Бекенд: Python 3.9, FastAPI, TensorFlow, OpenCV, Uvicorn, Docker.Фронтенд: React 18, TailwindCSS, Axios, Framer Motion.Додатково: Docker, Ngrok для тестування API.

🛠 Встановлення та запуск

🔹 Локальний запуск без Docker

Встановити залежності:

pip install -r requirements.txt
cd frontend && npm install

Запустити сервер:

uvicorn src.api.server:app --host 0.0.0.0 --port 8000

Запустити React-фронтенд:

cd frontend
npm start

Перевірити API в браузері: Відкрити http://127.0.0.1:8000/docs.

Відкрити UI: Відкрити http://127.0.0.1:3000.

🔹 Запуск у Docker

docker-compose up --build

🔹 Використання Ngrok (щоб отримати публічний доступ до фронтенду)

ngrok http 3000

🔥 API ендпоінти

POST /predict/ — приймає зображення, повертає передбачений клас та впевненість.

GET / — повертає HTML-сторінку фронтенду.

📜 TODO



