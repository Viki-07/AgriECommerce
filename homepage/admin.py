from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render
from .models import Product, Cart, Order, OrderItem

class HomepageAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', self.admin_view(self.dashboard_view), name='homepage-dashboard'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        context = {
            'total_products': Product.objects.count(),
            'total_orders': Order.objects.count(),
            'pending_orders': Order.objects.filter(status='pending').count(),
            'low_stock': Product.objects.filter(stock__lte=10).count(),
            'recent_orders': Order.objects.all().order_by('-created_at')[:5],
        }
        return render(request, 'admin/homepage/index.html', context)

    def admin_view(self, view):
        inner = super().admin_view(view)
        inner.is_admin_view = True
        return inner

site = HomepageAdminSite(name='admin')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'stock', 'created_at', 'image_preview')
    list_filter = ('category', 'created_at', 'stock')
    search_fields = ('name', 'category', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'image')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'stock')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('price',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'shipping_address')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]
    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'total_amount', 'status', 'shipping_address')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status == 'delivered':
            return self.readonly_fields + ('status',)
        return self.readonly_fields

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'ref_product', 'quantity', 'total_price', 'added_at')
    list_filter = ('added_at', 'user')
    search_fields = ('user__username', 'ref_product__name')
    readonly_fields = ('added_at',)

# Register models with our custom admin site
site.register(Product, ProductAdmin)
site.register(Order, OrderAdmin)
site.register(Cart, CartAdmin)