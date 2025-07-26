from rest_framework import serializers
from .models import Restaurant, MenuItem, Order, OrderItem


class RestaurantSerializer(serializers.ModelSerializer):
    """Serializer for Restaurant model"""
    menu_items_count = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'description', 'is_active', 'created_at', 'updated_at', 'menu_items_count']
        read_only_fields = ['created_at', 'updated_at']

    def get_menu_items_count(self, obj):
        return obj.menu_items.filter(is_available=True).count()


class MenuItemSerializer(serializers.ModelSerializer):
    """Serializer for MenuItem model"""
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'restaurant', 'restaurant_name', 'name', 'description', 'price', 
                 'is_available', 'category', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class OrderItemCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating OrderItem instances"""
    
    class Meta:
        model = OrderItem
        fields = ['menu_item', 'quantity', 'special_instructions']

    def validate(self, data):
        """Validate that the menu item belongs to the same restaurant as the order"""
        if hasattr(self, 'initial_data') and 'order' in self.context:
            order = self.context['order']
            menu_item = data['menu_item']
            if menu_item.restaurant != order.restaurant:
                raise serializers.ValidationError(
                    "Menu item must belong to the same restaurant as the order."
                )
        return data


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem model with full details"""
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)
    menu_item_description = serializers.CharField(source='menu_item.description', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'menu_item_name', 'menu_item_description', 
                 'quantity', 'unit_price', 'subtotal', 'special_instructions']
        read_only_fields = ['unit_price', 'subtotal']


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Order instances"""
    order_items = OrderItemCreateSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['restaurant', 'customer_name', 'table_number', 'notes', 'order_items']

    def create(self, validated_data):
        """Create order with associated order items"""
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        
        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        # Calculate and save total
        order.calculate_total()
        order.save()
        
        return order

    def validate_order_items(self, value):
        """Validate that order has at least one item"""
        if not value:
            raise serializers.ValidationError("Order must contain at least one item.")
        return value


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model with full details"""
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'restaurant', 'restaurant_name', 'customer_name', 'table_number', 'status', 
                 'status_display', 'total_amount', 'notes', 'order_items', 
                 'created_at', 'updated_at']
        read_only_fields = ['total_amount', 'created_at', 'updated_at']


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating only the order status"""
    
    class Meta:
        model = Order
        fields = ['status']

    def validate_status(self, value):
        """Validate status transitions"""
        if self.instance:
            current_status = self.instance.status
            # Define allowed transitions
            allowed_transitions = {
                'pending': ['in_progress', 'cancelled'],
                'in_progress': ['done', 'cancelled'],
                'done': [],  # No transitions from done
                'cancelled': []  # No transitions from cancelled
            }
            
            if value not in allowed_transitions.get(current_status, []):
                raise serializers.ValidationError(
                    f"Cannot change status from '{current_status}' to '{value}'"
                )
        return value 