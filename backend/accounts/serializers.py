from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "firebase_uid",
            "name",
            "email",
            "phone",
            "role",
            "is_active",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "firebase_uid",
            "email",
            "role",
            "is_active",
            "created_at",
        ]