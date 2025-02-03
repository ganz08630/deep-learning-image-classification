import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

def build_model():
    """
    Створює згорткову нейронну мережу для класифікації зображень CIFAR-10.
    """

    model = keras.Sequential([
        # 1-й шар: згортка + нормалізація + активація + пулінг
        layers.Conv2D(32, (3, 3), activation="relu", input_shape=(32, 32, 3)),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        # 2-й шар: згортка + нормалізація + активація + пулінг
        layers.Conv2D(64, (3, 3), activation="relu"),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        # 3-й шар: згортка + нормалізація + активація
        layers.Conv2D(128, (3, 3), activation="relu"),
        layers.BatchNormalization(),

        # Flatten - перетворюємо 3D-матрицю у вектор
        layers.Flatten(),

        # 4-й шар: прихований Dense + Dropout
        layers.Dense(128, activation="relu"),
        layers.Dropout(0.5),  # Запобігає перенавчанню

        # Вихідний шар: 10 класів, softmax для ймовірностей
        layers.Dense(10, activation="softmax")
    ])

    # Компілюємо модель
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model
