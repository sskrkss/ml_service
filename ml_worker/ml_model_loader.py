from typing import Any

import torch
from transformers import pipeline, Pipeline


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

    def _load_model(self) -> Pipeline:
        return pipeline(
            "text-classification",
            model="fyaronskiy/ruRoberta-large-ru-go-emotions",
            top_k=None
        )

    def predict(self, input_text: str) -> Any:
        return self._model(input_text)
