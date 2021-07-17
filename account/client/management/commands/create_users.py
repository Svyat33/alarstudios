import json
import logging
import os

import pika
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from client.serializers import UserChangesSerializer

User = get_user_model()
logger = logging.getLogger(__name__)



class Command(BaseCommand):
    help = 'Create test users'

    def handle(self, *args, **options):
        logger.info("Create test users")
        for i in range(5):
            username = f"user{i}"
            try:
                user = User.objects.create(username=username)
                user.set_password(username)
                user.save()
                logger.info(f"User: {username}\tpassword: {username}")
            except:
                logger.info(f"User {username} already exists.")
        logger.info("done")