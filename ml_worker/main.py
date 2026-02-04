import json
import logging
import os

import pika
import requests

from ml_model_loader import MlModelLoader

best_thresholds = {
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

emotions_dict = {
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

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

connection_params = pika.ConnectionParameters(
    host=os.getenv("RMQ_HOST"),
    port=int(os.getenv("RMQ_PORT")),
    virtual_host="/",
    credentials=pika.PlainCredentials(
        username=os.getenv("RMQ_USER"),
        password=os.getenv("RMQ_PASS")
    ),
    heartbeat=30,
    blocked_connection_timeout=2
)

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()
queue_name = os.getenv("RMQ_QUEUE")
channel.queue_declare(queue=queue_name)

ml_model = MlModelLoader()


def filter_predictions_by_threshold(predictions: list) -> list:
    """
    Фильтрует предсказания по порогам и возвращает только русские названия эмоций.

    Args:
        predictions: Список словарей с предсказаниями [{'label': 'emotion', 'score': 0.5}]

    Returns:
        list: Список русских названий эмоций, превысивших порог
    """
    russian_emotions = []

    for pred in predictions:
        label = pred['label']
        score = pred['score']

        # Проверяем превышает ли score порог для данной эмоции
        if label in best_thresholds and score >= best_thresholds[label]:
            # Переводим на русский и добавляем в список
            russian_label = emotions_dict.get(label, label)
            russian_emotions.append(russian_label)

    # Убираем дубликаты (на всякий случай)
    russian_emotions = list(dict.fromkeys(russian_emotions))

    return russian_emotions


def process_prediction(raw_predictions: list) -> list:
    """
    Обрабатывает предсказания модели.

    Args:
        raw_predictions: Сырые предсказания от модели

    Returns:
        list: Обработанные предсказания
    """
    if isinstance(raw_predictions, list) and len(raw_predictions) > 0:
        if isinstance(raw_predictions[0], list):
            predictions = raw_predictions[0]
        else:
            predictions = raw_predictions
    else:
        predictions = raw_predictions

    return filter_predictions_by_threshold(predictions)


def callback(ch, method, properties, body):
    message_str = body.decode("utf-8")
    message = json.loads(message_str)
    raw_prediction = ml_model.predict(message['input_text'])
    processed_prediction = process_prediction(raw_prediction)

    try:
        response = requests.post(
            f"{os.getenv('APP_URL')}/api/ml-tasks/save-prediction",
            json={
                "task_id": message["task_id"],
                "prediction": processed_prediction
            },
            timeout=30
        )

        if response.status_code == 200:
            results = response.json()
            logger.info(f"API response: {results}")
        else:
            logger.error(f"API error: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {e}")

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=False
)

channel.start_consuming()
