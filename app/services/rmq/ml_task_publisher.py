import json
from uuid import UUID

import pika

from database.config import get_settings

setting = get_settings()
connection_params = pika.ConnectionParameters(
    host=setting.RMQ_HOST,
    port=setting.RMQ_PORT,
    virtual_host='/',
    credentials=pika.PlainCredentials(
        username=setting.RMQ_USER,
        password=setting.RMQ_PASS
    ),
    heartbeat=30,
    blocked_connection_timeout=2
)


def send_task(task_id: UUID, input_text: str):
    message = {
        "task_id": str(task_id),
        "input_text": input_text
    }

    message_bytes = json.dumps(message).encode('utf-8')

    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    queue_name = setting.RMQ_QUEUE

    channel.queue_declare(queue=queue_name)

    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=message_bytes
    )

    connection.close()
