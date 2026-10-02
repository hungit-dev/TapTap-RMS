from django.db import models
from django.core.validators import MinValueValidator
from accounts.models import User
from dining.models import TableSession
from menu.models import MenuItem

class PromoCode(models.Model):
    DISCOUNT_CHOICES = [
           ("PERCENT","Percent"),
           ("FIXED","Fixed")
        ]
    code = models.CharField(max_length=30, unique=True)
    discount_type=models.CharField(max_length=20, choices=DISCOUNT_CHOICES,default="FIXED")
    discount_value = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0)],)
    min_amount = models.DecimalField(max_digits=10, decimal_places=2, null= True, blank= True)
    max_total_uses = models.PositiveIntegerField(null=True,blank=True)
    max_use_per_customer=models.PositiveIntegerField(null=True,blank=True)
    starts_at = models.DateTimeField()
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

class Order(models.Model):
    TYPE_CHOICES = [
        ("DINE_IN","Dine in"),
        ("ONLINE","Online")
    ]
    STATUS_CHOICES = [
        ("PLACED","Placed"),
        ("PREPARING","Preparing"),
        ("READY","Ready"),
        ("FOOD_SERVED","Food served"),
        ("OUT_FOR_DELIVERY","Out for delivery"),
        ("DELIVERED","Delivered"),
        ("COMPLETED", "Completed"),
        ("CANCELLED","Cancelled")
    ]
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="orders", null=True, blank=True)
    table_session = models.ForeignKey(TableSession, on_delete=models.PROTECT, related_name="orders", null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="created_orders", null=True, blank=True)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL,related_name="orders", null=True, blank=True)
    order_number = models.CharField(max_length=20, unique = True)
    order_type= models.CharField(max_length=30, choices=TYPE_CHOICES)
    status = models.CharField(max_length=30, choices = STATUS_CHOICES, default = "PLACED")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    preparing_started_at = models.DateTimeField(null=True,blank=True)
    ready_at = models.DateTimeField(null=True,blank=True)
    food_served_at = models.DateTimeField(null=True,blank=True) # for dine-in orders only
    completed_at = models.DateTimeField(null=True,blank=True)
    cancelled_at = models.DateTimeField(null=True,blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order {self.order_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT,related_name="order_items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL,null=True, related_name="order_items")
    item_name = models.CharField(max_length=30)
    unit_price = models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(0.01)])
    quantity = models.PositiveBigIntegerField( validators=[MinValueValidator(1)])
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.order.order_number} - {self.item_name} x {self.quantity}"