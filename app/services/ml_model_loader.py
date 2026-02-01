import pickle
from typing import Any

import pandas as pd


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

    # TODO: Урок 5. model_path инжектим через env, плюс обработка ошибок
    # TODO: Урок 5. Any мне не нравится, нужно понять, что по факту будет возвращаться
    def _load_model(self) -> Any:
        model_path = "models/random_forest.pkl"

        with open(model_path, 'rb') as f:
            return pickle.load(f)

    # TODO: Урок 5. трай кетч точно нужен
    def predict(self, features: pd.Dataset):
        return self._model.predict(features)
