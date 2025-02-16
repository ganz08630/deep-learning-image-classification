from src.dataset_loader import load_dataset

# Завантажуємо датасет
train_data, test_data, dataset_info = load_dataset()

# Виводимо інформацію про датасет
print(f"Кількість класів: {dataset_info.features['label'].num_classes}")
print(f"Назви класів: {dataset_info.features['label'].names}")

# Перевіряємо першу партію зображень
for images, labels in train_data.take(1):
    print(f"Розмір batch: {images.shape}")
    print(f"Мітки: {labels.numpy()}")
