from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from client.serializers import UserListSerializer

User = get_user_model()


class AccountView(mixins.ListModelMixin, GenericViewSet):
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.exclude(is_superuser=True)
