from typing import Any, List

import torch
from transformers import pipeline, Pipeline


class MlModel:
    _instance = None
    _model = None

    _best_thresholds = {
        'admiration': 0.36734693877551017,
        'amusement': 0.2857142857142857,
        'anger': 0.2857142857142857,
        'annoyance': 0.16326530612244897,
        'approval': 0.14285714285714285,
        'caring': 0.14285714285714285,
        'confusion': 0.18367346938775508,
        'curiosity': 0.3469387755102041,
        'desire': 0.32653061224489793,
        'disappointment': 0.22448979591836732,
        'disapproval': 0.2040816326530612,
        'disgust': 0.2857142857142857,
        'embarrassment': 0.18367346938775508,
        'excitement': 0.2857142857142857,
        'fear': 0.24489795918367346,
        'gratitude': 0.7142857142857142,
        'grief': 0.02040816326530612,
        'joy': 0.3061224489795918,
        'love': 0.44897959183673464,
        'nervousness': 0.061224489795918366,
        'optimism': 0.18367346938775508,
        'pride': 0.04081632653061224,
        'realization': 0.08163265306122448,
        'relief': 0.1020408163265306,
        'remorse': 0.22448979591836732,
        'sadness': 0.3877551020408163,
        'surprise': 0.3469387755102041,
        'neutral': 0.24489795918367346
    }

    _ru_labels = {
        "admiration": "восхищение",
        "amusement": "веселье",
        "anger": "злость",
        "annoyance": "раздражение",
        "approval": "одобрение",
        "caring": "забота",
        "confusion": "непонимание",
        "curiosity": "любопытство",
        "desire": "желание",
        "disappointment": "разочарование",
        "disapproval": "неодобрение",
        "disgust": "отвращение",
        "embarrassment": "смущение",
        "excitement": "возбуждение",
        "fear": "страх",
        "gratitude": "признательность",
        "grief": "горе",
        "joy": "радость",
        "love": "любовь",
        "nervousness": "нервозность",
        "optimism": "оптимизм",
        "pride": "гордость",
        "realization": "осознание",
        "relief": "облегчение",
        "remorse": "раскаяние",
        "sadness": "грусть",
        "surprise": "удивление",
        "neutral": "нейтральность"
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
            model="fyaronskiy/ruRoberta-large-ru-go-emotions",
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
                ru_label = self._ru_labels[label]
                processed_predictions.append(ru_label)

        return processed_predictions

    def predict(self, input_text: str) -> List[str]:
        self._validate_input_text(input_text=input_text)

        raw_predictions = self._model(input_text)

        return self._process_raw_predictions(raw_predictions)
