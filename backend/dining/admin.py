from django.contrib import admin
from .models import Table, TableSession

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("table_number","capacity","status","is_active")
    list_filter = ("status","is_active")
    search_fields = ("table_number",)

@admin.register(TableSession)
class TableSessionAdmin(admin.ModelAdmin):
    list_display = ("table", "staff", "seated_at", "closed_at")
    list_filter = ("seated_at", "closed_at")

 