from typing import Any, List

import torch
from transformers import pipeline, Pipeline


class MlModel:
    _instance = None
    _model = None

    _best_thresholds = {
        'admiration': 0.25,
        'amusement': 0.45,
        'anger': 0.15,
        'annoyance': 0.10,
        'approval': 0.30,
        'caring': 0.40,
        'confusion': 0.55,
        'curiosity': 0.25,
        'desire': 0.25,
        'disappointment': 0.40,
        'disapproval': 0.30,
        'disgust': 0.20,
        'embarrassment': 0.10,
        'excitement': 0.35,
        'fear': 0.40,
        'gratitude': 0.45,
        'grief': 0.05,
        'joy': 0.40,
        'love': 0.25,
        'nervousness': 0.25,
        'optimism': 0.20,
        'pride': 0.10,
        'realization': 0.15,
        'relief': 0.05,
        'remorse': 0.10,
        'sadness': 0.40,
        'surprise': 0.15,
        'neutral': 0.25
    }

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
            model="SamLowe/roberta-base-go_emotions",
            top_k=None
        )

    def _validate_input_text(self, input_text: str) -> None:
        if len(input_text) > 200:
            raise ValueError("Text exceeds maximum length of 200 characters")

    def _process_raw_predictions(self, raw_predictions: List[Any]) -> List[str]:
        if not raw_predictions:
            return []

        processed_predictions = []

        for raw_prediction in raw_predictions[0]:
            label = raw_prediction['label']
            score = raw_prediction['score']

            if label in self._best_thresholds and score >= self._best_thresholds[label]:
                processed_predictions.append(label)

        return processed_predictions

    def predict(self, input_text: str) -> List[str]:
        self._validate_input_text(input_text=input_text)

        raw_predictions = self._model(input_text)

        return self._process_raw_predictions(raw_predictions)
