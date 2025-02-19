import sqlite3
import os

# Визначаємо шлях до БД відносно src
DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

def create_table():
    """Створює таблицю predictions, якщо її немає"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            username TEXT,
            file_path TEXT NOT NULL,
            prediction TEXT NOT NULL,
            confidence REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def save_prediction(user_id, username, file_path, prediction, confidence):
    """Зберігає результат класифікації в БД"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions (user_id, username, file_path, prediction, confidence)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, username, file_path, prediction, confidence))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_table()
    print(f"✅ База даних ініціалізована в {DB_PATH}")
