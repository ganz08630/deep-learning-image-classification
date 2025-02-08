import tensorflow as tf
import tensorflow_datasets as tfds
import numpy as np
import cv2
import os

# Шлях до моделі
MODEL_PATH = "models/cifar10_model.h5"

# Завантажуємо класи CIFAR-10
CLASS_NAMES = tfds.builder("cifar10").info.features["label"].names

# Завантажуємо модель (щоб не завантажувати щоразу при API-запиті)
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"❌ Помилка: Файл {MODEL_PATH} не знайдено!")

model = tf.keras.models.load_model(MODEL_PATH)
print("✅ Модель завантажено успішно!")

def preprocess_image(image):
    """
    Приймає зображення у форматі OpenCV (NumPy) або PIL, змінює розмір та нормалізує.
    """
    if isinstance(image, np.ndarray):  # Якщо це OpenCV (NumPy)
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Конвертуємо в RGB
    else:  # Якщо це об'єкт PIL
        img = np.array(image)

    img = cv2.resize(img, (32, 32))  # CIFAR-10 має розмір 32x32
    img = img / 255.0  # Нормалізуємо
    img = np.expand_dims(img, axis=0)  # Додаємо batch dimension
    return img

def predict_image(image):
    """
    Отримує зображення (NumPy/PIL), передбачає клас і повертає його.
    """
    img = preprocess_image(image)
    predictions = model.predict(img)
    predicted_class = np.argmax(predictions[0])  # Отримуємо індекс найвищого значення
    confidence = predictions[0][predicted_class] * 100  # Впевненість у %
    return CLASS_NAMES[predicted_class], confidence
