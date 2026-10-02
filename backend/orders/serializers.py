from rest_framework import serializers
from .models import PromoCode, Order, OrderItem
from .services import calculate_order_totals
from django.db import transaction

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


    
class OrderSerializer(serializers.ModelSerializer):
    # get all items that belong to an order and put them in a list
    items = OrderItemSerializer(
        many=True,
        source="order_items"
    )

    class Meta:
        model=Order
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_by",
        ]

    def create(self, validated_data):
        # Remove items because it is not an Order model field
        items_data = validated_data.pop("order_items")
        # Use a transaction so that any error rolls back all changes.
        with transaction.atomic():
            # Create the order
            order = Order.objects.create(**validated_data)

            # Create the order items
            for item_data in items_data:
                OrderItem.objects.create(
                    order=order,
                    menu_item=item_data["menu_item"],
                    item_name=item_data["menu_item"].name,
                    unit_price=item_data["menu_item"].price,
                    quantity=item_data["quantity"],
                    notes=item_data.get("notes", "")
                )

            # Calculate order totals
            subtotal, discount_amount, tax_amount, total = (
                calculate_order_totals(
                    order,
                    tax_percentage=5 # Alberta current tax
                )
            )

            # Save calculated totals
            order.subtotal = subtotal
            order.discount_amount = discount_amount
            order.tax_amount = tax_amount
            order.total = total

            order.save()

        return order
