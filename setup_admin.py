#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'waiterapi.settings')
django.setup()

from django.contrib.auth.models import User
from orders.models import Restaurant, MenuItem, Order, OrderItem
from decimal import Decimal

def setup_admin_user():
    """Create admin user if it doesn't exist"""
    if not User.objects.filter(username='admin').exists():
        print("Creating admin user...")
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print("Admin user created! Username: admin, Password: admin123")
    else:
        print("Admin user already exists")

def create_sample_data():
    """Create sample data if none exists"""
    if Restaurant.objects.count() > 0:
        print("Sample data already exists")
        return
        
    print("Creating sample data...")
    
    # Create restaurants
    pizza_place = Restaurant.objects.create(
        name="Mario's Pizza",
        description="Authentic Italian pizza and pasta"
    )
    
    burger_joint = Restaurant.objects.create(
        name="Burger Palace",
        description="Gourmet burgers and fries"
    )
    
    sushi_bar = Restaurant.objects.create(
        name="Sakura Sushi",
        description="Fresh sushi and Japanese cuisine"
    )
    
    # Create menu items for Pizza Place
    MenuItem.objects.create(
        restaurant=pizza_place,
        name="Margherita Pizza",
        description="Fresh tomato sauce, mozzarella, and basil",
        price=Decimal('15.99'),
        category="Pizza"
    )
    
    MenuItem.objects.create(
        restaurant=pizza_place,
        name="Pepperoni Pizza",
        description="Classic pepperoni with mozzarella cheese",
        price=Decimal('17.99'),
        category="Pizza"
    )
    
    MenuItem.objects.create(
        restaurant=pizza_place,
        name="Caesar Salad",
        description="Crisp romaine lettuce with caesar dressing",
        price=Decimal('9.99'),
        category="Salad"
    )
    
    # Create menu items for Burger Joint
    MenuItem.objects.create(
        restaurant=burger_joint,
        name="Classic Cheeseburger",
        description="Beef patty with cheese, lettuce, tomato",
        price=Decimal('12.99'),
        category="Burger"
    )
    
    MenuItem.objects.create(
        restaurant=burger_joint,
        name="French Fries",
        description="Crispy golden fries",
        price=Decimal('5.99'),
        category="Side"
    )
    
    MenuItem.objects.create(
        restaurant=burger_joint,
        name="Chocolate Shake",
        description="Rich chocolate milkshake",
        price=Decimal('6.99'),
        category="Drink"
    )
    
    # Create menu items for Sushi Bar
    MenuItem.objects.create(
        restaurant=sushi_bar,
        name="Salmon Roll",
        description="Fresh salmon with rice and nori",
        price=Decimal('8.99'),
        category="Sushi"
    )
    
    MenuItem.objects.create(
        restaurant=sushi_bar,
        name="California Roll",
        description="Crab, avocado, and cucumber",
        price=Decimal('7.99'),
        category="Sushi"
    )
    
    MenuItem.objects.create(
        restaurant=sushi_bar,
        name="Miso Soup",
        description="Traditional Japanese soup",
        price=Decimal('3.99'),
        category="Soup"
    )
    
    print(f"Created {Restaurant.objects.count()} restaurants")
    print(f"Created {MenuItem.objects.count()} menu items")
    print("Sample data created successfully!")

if __name__ == "__main__":
    setup_admin_user()
    create_sample_data() 