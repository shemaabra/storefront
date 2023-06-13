from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreateSerializer as BaseUserCreateSerilizer,
)
from rest_framework import serializers


class UserCreateSerializer(BaseUserCreateSerilizer):
    dob = serializers.DateField(read_only=True)

    class Meta(BaseUserCreateSerilizer.Meta):
        fields = [
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "dob",
        ]


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ["id", "username", "email", "first_name", "last_name"]
