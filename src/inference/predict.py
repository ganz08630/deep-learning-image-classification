import tensorflow as tf
import tensorflow_datasets as tfds
import numpy as np
import cv2
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'datasets'))
from dataset_loader import load_dataset

# Шлях до моделі
MODEL_PATH = "models/cifar10_model.h5"

# Завантажуємо класи CIFAR-10
CLASS_NAMES = tfds.builder("cifar10").info.features["label"].names

def load_and_preprocess_image(image_path):
    """
    Завантажує зображення, змінює його розмір та перетворює у формат тензору.
    """
    if not os.path.exists(image_path):
        print(f"❌ Помилка: Файл {image_path} не знайдено!")
        sys.exit(1)

    img = cv2.imread(image_path)  # Завантажуємо зображення
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Конвертуємо у RGB
    img = cv2.resize(img, (32, 32))  # Змінюємо розмір до 32x32
    img = img / 255.0  # Нормалізуємо пікселі (0-1)
    img = np.expand_dims(img, axis=0)  # Додаємо вимір batch_size

    return img

def predict(image_path):
    """
    Завантажує модель і робить передбачення для зображення.
    """
    if not os.path.exists(MODEL_PATH):
        print(f"❌ Помилка: Файл {MODEL_PATH} не знайдено! Спочатку запусти train.py")
        return

    model = tf.keras.models.load_model(MODEL_PATH)
    print("✅ Модель завантажено успішно!")

    # Обробляємо зображення
    img = load_and_preprocess_image(image_path)

    # Робимо передбачення
    predictions = model.predict(img)
    predicted_class = np.argmax(predictions[0])  # Отримуємо індекс найвищого значення

    print(f"🔍 Передбачений клас: {CLASS_NAMES[predicted_class]}")
    print(f"📊 Впевненість: {predictions[0][predicted_class] * 100:.2f}%")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Використання: python src/predict.py /шлях/до/зображення.jpg")
        sys.exit(1)

    image_path = sys.argv[1]
    predict(image_path)
