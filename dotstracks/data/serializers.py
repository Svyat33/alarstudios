import logging
from rest_framework import serializers
from django.contrib.auth import get_user_model

from data.models import Dot, Track

User = get_user_model()
logger = logging.getLogger(__name__)


class UserChangesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "is_active",
            "is_superuser",
        ]


class UserSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
        ]


class DotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dot
        fields = "__all__"


class TrackSerializerList(serializers.ModelSerializer):
    user = UserSmallSerializer(read_only=True)
    begin = DotSerializer(read_only=True)
    end = DotSerializer(read_only=True)

    class Meta:
        model = Track
        fields = ['id','name', 'user', 'length', 'begin', 'end']

class TrackDetailSerializer(serializers.ModelSerializer):
    user = UserSmallSerializer(read_only=True)
    track = DotSerializer(read_only=True, many=True)
    class Meta:
        model = Track
        fields = ['id', 'name', 'user', 'length', 'track',]

class TrackCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['name', 'length',]