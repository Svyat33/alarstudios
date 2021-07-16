from django.apps import AppConfig


class ClientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'client'

    def ready(self):
        from django.contrib.auth import get_user_model
        from client.models import publish_user
        User = get_user_model()
        for u in User.objects.all():
            publish_user(u)
