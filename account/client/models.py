import logging

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from client.notifier import publish

logger = logging.getLogger(__name__)


class User(AbstractUser):
    tracks_length = models.IntegerField(default=0)
    tracks_qty = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.pk}: {self.username}' + (' [!]' if self.is_superuser else '')


def publish_user_created(user: User) -> None:
    logger.info(f"send user {user} to channel")
    publish('user_stored', {'id': user.pk, 'username': user.username, 'is_superuser': user.is_superuser, 'is_active': user.is_active})


@receiver(post_save, sender=User)
def notify_about_new_user(instance: User, created, *args, **kwargs) -> None:
    if created:
        publish_user_created(instance)

def publish_user_deleted(user: User) -> None:
    logger.info(f"send user {user} to channel")
    publish('user_deleted', {'id': user.pk})

@receiver(post_delete, sender=User)
def motify_user_deleted(instance: User, *args, **kwargs) -> None:
    print(instance, args, kwargs)
