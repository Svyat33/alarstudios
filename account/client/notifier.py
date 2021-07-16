import json
import logging
import os

import pika
from pika.exceptions import AMQPConnectionError

logger = logging.getLogger(__name__)


def publish(method, body):
    params = pika.URLParameters(os.getenv('RABITMQ_CONNECT'))
    try:
        connection = pika.BlockingConnection(params)
    except AMQPConnectionError as e:
        logger.error(f"Cant connect to ampq server `{e}`!")
        return
    channel = connection.channel()

    properties = pika.BasicProperties(method)
    try:
        msg = json.dumps(body)
    except TypeError as e:
        logger.error(f"Wrong data to publish `{e}`")
        return
    channel.basic_publish(exchange='', routing_key=os.getenv('ACCOUNT_TOPIC'), body=msg, properties=properties)
