import tensorflow as tf
import os
from dataset_loader import load_dataset

# Шлях до збереженої моделі
MODEL_PATH = "models/cifar10_model.h5"

def evaluate():
    """
    Завантажуємо модель і тестуємо її на валідаційному датасеті.
    """

    # Завантажуємо датасет
    _, test_data, class_names = load_dataset(batch_size=64)

    # Завантажуємо модель
    if not os.path.exists(MODEL_PATH):
        print(f"Помилка: Файл {MODEL_PATH} не знайдено! Спочатку запусти train.py")
        return

    model = tf.keras.models.load_model(MODEL_PATH)
    print("✅ Модель завантажено успішно!")

    # Оцінюємо точність
    loss, accuracy = model.evaluate(test_data)
    print(f"🎯 Точність моделі: {accuracy * 100:.2f}%")

if __name__ == "__main__":
    evaluate()
