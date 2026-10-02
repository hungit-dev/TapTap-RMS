from rest_framework import serializers
from .models import Table, TableSession

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'
        read_only_fields = ("id","status", "created_at", "updated_at")


class TableSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableSession
        fields = '__all__'
        read_only_fields = ("id","staff", "seated_at", "closed_at")