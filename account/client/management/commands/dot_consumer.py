import json
import logging
import os

import pika
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from client.serializers import UserChangesSerializer

User = get_user_model()
logger = logging.getLogger(__name__)


def callback(ch, method, properties, body):
    data = json.loads(body)
    if properties.content_type == 'track_stored':
        try:
            i = User.objects.get(pk=data.get('id'))
        except:
            return
        serializer = UserChangesSerializer(data=data, instance=i)
        if serializer.is_valid():
            usr = serializer.save()
            logger.info(f"Updated user {usr}")


class Command(BaseCommand):
    help = 'Listen new users and user changes'

    def handle(self, *args, **options):
        print(os.getenv('RABITMQ_CONNECT'), os.getenv('TRACK_CREATE_TOPIC'))
        params = pika.URLParameters(os.getenv('RABITMQ_CONNECT'))
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue=os.getenv('TRACK_CREATE_TOPIC'))
        channel.basic_consume(queue=os.getenv('TRACK_CREATE_TOPIC'), on_message_callback=callback, auto_ack=True)
        logger.info(f"Start cunsuming channel {os.getenv('TRACK_CREATE_TOPIC')}")
        try:
            channel.start_consuming()
        finally:
            channel.close()
