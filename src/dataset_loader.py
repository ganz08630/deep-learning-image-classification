import tensorflow as tf
import tensorflow_datasets as tfds

# Завантаження CIFAR-10
def load_dataset(batch_size=32, shuffle_buffer_size=1000):
    """
    Завантажує датасет CIFAR-10, нормалізує дані та готує для тренування.
    """

    # Завантажуємо датасет
    (train_data, test_data), dataset_info = tfds.load(
        "cifar10",
        split=["train", "test"],
        as_supervised=True,  # Повертає (зображення, мітку)
        with_info=True  # Повертає також інформацію про датасет
    )

    # Нормалізація зображень (перетворення значень пікселів [0,255] у [0,1])
    def normalize_img(image, label):
        return tf.cast(image, tf.float32) / 255.0, label

    # Застосовуємо нормалізацію
    train_data = train_data.map(normalize_img).shuffle(shuffle_buffer_size).batch(batch_size)
    test_data = test_data.map(normalize_img).batch(batch_size)

    return train_data, test_data, dataset_info
