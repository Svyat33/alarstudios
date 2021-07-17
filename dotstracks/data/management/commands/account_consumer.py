import json
import logging
import os

import pika
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from data.serializers import UserChangesSerializer

User = get_user_model()
logger = logging.getLogger(__name__)


def callback(ch, method, properties, body):
    data = json.loads(body)
    if 'user_stored' == properties.content_type:
        serializer = UserChangesSerializer(data=data)
        if serializer.is_valid():
            usr = serializer.save()
            logger.info(f"Create user {usr}")
    elif 'user_deleted' == properties.content_type:
        logger.info(f"User {data['id']} deleted")
        User.objects.filter(pk=data.get('id')).delete()

class Command(BaseCommand):
    help = 'Listen new users and user changes'

    def handle(self, *args, **options):
        print(os.getenv('RABITMQ_CONNECT'), os.getenv('ACCOUNT_TOPIC'))
        params = pika.URLParameters(os.getenv('RABITMQ_CONNECT'))
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue=os.getenv('ACCOUNT_TOPIC'))
        channel.basic_consume(queue=os.getenv('ACCOUNT_TOPIC'), on_message_callback=callback, auto_ack=True)
        logger.info(f"Start cunsuming channel {os.getenv('ACCOUNT_TOPIC')}")
        try:
            channel.start_consuming()
        finally:
            channel.close()
