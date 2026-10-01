from django.contrib import admin
from .models import PromoCode, Order, OrderItem

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'expires_at', 'is_active')
    list_filter = ('is_active', 'discount_type')
    search_fields = ('code',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "order_type", "status", "customer", "total", "created_at")
    list_filter = ("order_type", "status")
    search_fields = ("order_number", "customer__email")

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order","item_name","unit_price","notes")
    list_filter = ("order__status","menu_item")
    search_fields = ("item_name","order__order_number")