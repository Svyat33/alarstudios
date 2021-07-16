import logging

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()
logger = logging.getLogger(__name__)


class UserChangesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "tracks_length",
            "tracks_qty",
        ]

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "tracks_length",
            "tracks_qty",
        ]