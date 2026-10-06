from rest_framework import serializers
from .models import Table, TableSession

class TableSerializer(serializers.ModelSerializer):
    active_session = serializers.SerializerMethodField()

    class Meta:
        model = Table
        fields = '__all__'
        read_only_fields = ("id","status", "created_at", "updated_at")

    # custom method to get the active session for the table
    def get_active_session(self, obj):
            session = obj.sessions.filter(
                closed_at__isnull=True
            ).first()
            if session:
                return TableSessionSerializer(session).data
            return None

class TableSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableSession
        fields = '__all__'
        read_only_fields = ("id","staff", "seated_at", "closed_at")