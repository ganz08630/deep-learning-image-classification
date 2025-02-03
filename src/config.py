import os

# Шлях до датасету
DATASET_PATH = os.getenv("DATASET_PATH", "data/dataset")

# Налаштування для навчання моделі
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 32))
EPOCHS = int(os.getenv("EPOCHS", 10))
LEARNING_RATE = float(os.getenv("LEARNING_RATE", 0.001))

# Шлях для збереження моделі
MODEL_SAVE_PATH = os.getenv("MODEL_SAVE_PATH", "models/model.h5")

# Класи датасету
CLASS_NAMES = ["cat", "dog"]  # Або завантажувати автоматично