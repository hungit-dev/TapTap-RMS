from rest_framework import serializers
from .models import PromoCode, Order, OrderItem

class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model= PromoCode
        fields = "__all__"

    def validate_code(self, value):
        return value.strip().upper()

    def validate(self, data):
        if data.get("discount_type") == "PERCENT" and data.get("discount_value", 0) > 100:
            raise serializers.ValidationError("Percent discount cannot be more than 100.")

        if data.get("starts_at") and data.get("expires_at"):
            if data["expires_at"] <= data["starts_at"]:
                raise serializers.ValidationError("Expiry must be after the start date.")
            
        return data

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_by",
        ]
   

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields ="__all__"
        read_only_fields = [
            "id",
            "order",
            "item_name",
            "unit_price",
        ]

    def validate_menu_item(self, value):
        if not value.is_available:
            raise serializers.ValidationError(
                "This menu item is not currently available."
            )
        return value

    def validate_order(self, value):
        if value.status in ["COMPLETED", "CANCELLED"]:
            raise serializers.ValidationError(
                "Cannot add items to a completed or cancelled order."
            )
        return value

    def create(self, validated_data):
        menu_item = validated_data["menu_item"]

        validated_data["item_name"] = menu_item.name
        validated_data["unit_price"] = menu_item.price

        return super().create(validated_data)