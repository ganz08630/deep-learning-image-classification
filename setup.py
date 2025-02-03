from setuptools import setup, find_packages

setup(
    name="image_classifier",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "tensorflow",
        "numpy",
        "matplotlib",
        "pandas",
        "scikit-learn"
    ],
    entry_points={
        "console_scripts": [
            "train=src.train:main",
            "predict=src.predict:main"
        ]
    },
)
