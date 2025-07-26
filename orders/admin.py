from django.contrib import admin
from .models import Restaurant, MenuItem, Order, OrderItem


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'restaurant', 'price', 'category', 'is_available']
    list_filter = ['restaurant', 'category', 'is_available', 'created_at']
    search_fields = ['name', 'description', 'restaurant__name']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['price', 'is_available']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['unit_price', 'subtotal']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'table_number', 'restaurant', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'restaurant', 'created_at']
    search_fields = ['customer_name', 'restaurant__name']
    readonly_fields = ['total_amount', 'created_at', 'updated_at']
    list_editable = ['status']
    inlines = [OrderItemInline]

    def save_related(self, request, form, formsets, change):
        """Override to recalculate total when order items change"""
        super().save_related(request, form, formsets, change)
        form.instance.calculate_total()
        form.instance.save()


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'menu_item', 'quantity', 'unit_price', 'subtotal']
    list_filter = ['order__restaurant', 'menu_item__category']
    search_fields = ['order__customer_name', 'menu_item__name']
    readonly_fields = ['unit_price', 'subtotal']
