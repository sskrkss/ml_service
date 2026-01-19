import pickle
from typing import Any

import pandas as pd


# TODO: проверить, что это действительно синглтон, нам не нужно хранить в памяти много моделей
class MlModelLoader:
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._model is None:
            self._model = self._load_model()

    # TODO: model_path инжектим через env, плюс обработка ошибок
    # TODO: Any мне не нравится, но пока так
    def _load_model(self) -> Any:
        model_path = "models/random_forest.pkl"

        with open(model_path, 'rb') as f:
            return pickle.load(f)

    # TODO: трай кетч точно нужен
    def predict(self, features: pd.Dataset):
        return self._model.predict(features)
