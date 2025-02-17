from django.contrib import admin

# Register your models here.
from .models import Product,Cart

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'stock', 'created_at')
    search_fields = ('name', 'category')

# admin.site.register(Product)
admin.site.register(Cart)