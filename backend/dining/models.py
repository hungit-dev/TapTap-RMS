from django.db import models
from accounts.models import User

class Table(models.Model):
    STATUS_CHOICES = [
        ("AVAILABLE", "Available"),
        ("OCCUPIED", "Occupied"),
    ]
    table_number = models.PositiveIntegerField(unique=True)
    capacity = models.PositiveIntegerField(default=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="AVAILABLE"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ["table_number"]

    def __str__(self):
        return f"Table {self.table_number}"


class TableSession(models.Model):
    table = models.ForeignKey(Table, on_delete=models.PROTECT, related_name="sessions")
    staff = models.ForeignKey(User, on_delete=models.PROTECT, related_name="table_sessions")
    seated_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return f"Table {self.table.table_number} - {self.staff.name}"