from django.db import models

class User(models.Model):
    firebase_uid = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    ROLE_CHOICES = [
        ("CUSTOMER", "Customer"),
        ("SERVER", "Server"),
        ("KITCHEN", "Kitchen"),
        ("DRIVER", "Driver"),
        ("MANAGER", "Manager"),
    ]
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.email