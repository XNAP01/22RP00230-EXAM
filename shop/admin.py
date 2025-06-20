from django.contrib import admin
from .models import Product, Order, OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'payment_method', 'status', 'date_ordered']
    list_filter = ['status', 'payment_method']
    search_fields = ['full_name', 'id']
    ordering = ['-date_ordered']

admin.site.register(Order, OrderAdmin)
admin.site.register(Product)
admin.site.register(OrderItem)