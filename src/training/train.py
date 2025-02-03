import tensorflow as tf
import os
from dataset_loader import load_dataset
from model_builder import build_model

# Параметри тренування
BATCH_SIZE = 64
EPOCHS = 10
MODEL_SAVE_PATH = "models/cifar10_model.h5"

def train():
    """
    Тренуємо модель CNN на датасеті CIFAR-10.
    """

    # Завантажуємо датасет
    train_data, test_data, _ = load_dataset(batch_size=BATCH_SIZE)

    # Створюємо модель
    model = build_model()

    # Додаємо Callbacks (збереження моделі та ранній стоп)
    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(MODEL_SAVE_PATH, save_best_only=True),
        tf.keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True)
    ]

    # Запускаємо тренування
    history = model.fit(
        train_data,
        epochs=EPOCHS,
        validation_data=test_data,
        callbacks=callbacks
    )

    # Зберігаємо модель
    model.save(MODEL_SAVE_PATH)
    print(f"Модель збережено в {MODEL_SAVE_PATH}")

if __name__ == "__main__":
    train()
