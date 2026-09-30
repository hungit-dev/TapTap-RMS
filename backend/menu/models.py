from django.db import models

class MenuCategory(models.Model):
    name = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField(default=0)
    is_active= models.BooleanField(default=True)

    class Meta: 
        ordering = ['display_order','name']
        verbose_name_plural = 'menu categories'

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    category = models.ForeignKey(MenuCategory, on_delete=models.PROTECT, related_name="menu_items")
    name = models.CharField(max_length=100)
    description= models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.name