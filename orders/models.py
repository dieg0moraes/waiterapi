from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Restaurant(models.Model):
    """Model representing a restaurant in the food court"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """Model representing menu items for each restaurant"""
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    is_available = models.BooleanField(default=True)
    category = models.CharField(max_length=50, blank=True)  # e.g., "Main", "Dessert", "Drink"
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['restaurant', 'category', 'name']
        unique_together = ['restaurant', 'name']

    def __str__(self):
        return f"{self.restaurant.name} - {self.name}"


class Order(models.Model):
    """Model representing customer orders"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    customer_name = models.CharField(max_length=100)
    table_number = models.CharField(max_length=10, blank=True, null=True, help_text="Table number for the order")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name} at {self.restaurant.name}"

    def calculate_total(self):
        """Calculate total amount from order items"""
        total = sum(item.subtotal for item in self.order_items.all())
        self.total_amount = total
        return total


class OrderItem(models.Model):
    """Model representing individual items in an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    special_instructions = models.TextField(blank=True)

    class Meta:
        unique_together = ['order', 'menu_item']

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name} for Order #{self.order.id}"

    def save(self, *args, **kwargs):
        """Override save to calculate subtotal automatically"""
        self.unit_price = self.menu_item.price
        self.subtotal = self.unit_price * self.quantity
        super().save(*args, **kwargs)
        # Update order total after saving order item
        self.order.calculate_total()
        self.order.save()
