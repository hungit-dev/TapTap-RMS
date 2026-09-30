from rest_framework import serializers
from .models import Table, TableSession

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'


class TableSessionSerializer(serializers.ModelSerializer):
    def validate_staff(self, user):
        if user.role not in ["SERVER", "MANAGER"]:
            raise serializers.ValidationError(
                "User must have the SERVER or MANAGER role."
            )
        return user
    
    class Meta:
        model = TableSession
        fields = '__all__'