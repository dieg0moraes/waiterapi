#!/usr/bin/env python
import os
import sys
import django
import json
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'waiterapi.settings')
django.setup()

from orders.models import Restaurant, MenuItem, Order, OrderItem
from django.contrib.auth.models import User

def generate_test_data():
    """Generate comprehensive test data for all entities"""
    
    # Clear existing data (optional)
    print("Clearing existing data...")
    OrderItem.objects.all().delete()
    Order.objects.all().delete()
    MenuItem.objects.all().delete()
    Restaurant.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()
    
    # Create admin user
    print("Creating admin user...")
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
    
    # Create restaurants
    print("Creating restaurants...")
    restaurants_data = [
        {
            'name': "Mario's Pizza Palace",
            'description': "Authentic Italian pizza and pasta since 1985",
            'is_active': True
        },
        {
            'name': "Burger Junction",
            'description': "Gourmet burgers and American classics",
            'is_active': True
        },
        {
            'name': "Sakura Sushi Bar",
            'description': "Fresh sushi and Japanese cuisine",
            'is_active': True
        },
        {
            'name': "Taco Fiesta",
            'description': "Authentic Mexican tacos and burritos",
            'is_active': True
        },
        {
            'name': "Golden Dragon",
            'description': "Traditional Chinese dishes and dim sum",
            'is_active': True
        },
        {
            'name': "Pasta Corner",
            'description': "Fresh Italian pasta and Mediterranean cuisine",
            'is_active': False  # Temporarily closed
        }
    ]
    
    restaurants = []
    for rest_data in restaurants_data:
        restaurant = Restaurant.objects.create(**rest_data)
        restaurants.append(restaurant)
    
    # Create menu items for each restaurant
    print("Creating menu items...")
    
    # Mario's Pizza Palace menu
    pizza_items = [
        {'name': 'Margherita Pizza', 'description': 'Fresh tomato sauce, mozzarella, basil', 'price': '15.99', 'category': 'Pizza'},
        {'name': 'Pepperoni Pizza', 'description': 'Classic pepperoni with mozzarella cheese', 'price': '17.99', 'category': 'Pizza'},
        {'name': 'Supreme Pizza', 'description': 'Pepperoni, sausage, mushrooms, peppers, onions', 'price': '21.99', 'category': 'Pizza'},
        {'name': 'Hawaiian Pizza', 'description': 'Ham, pineapple, mozzarella cheese', 'price': '18.99', 'category': 'Pizza'},
        {'name': 'Caesar Salad', 'description': 'Crisp romaine lettuce with caesar dressing', 'price': '9.99', 'category': 'Salad'},
        {'name': 'Garlic Bread', 'description': 'Fresh bread with garlic butter', 'price': '6.99', 'category': 'Appetizer'},
        {'name': 'Spaghetti Carbonara', 'description': 'Creamy pasta with bacon and parmesan', 'price': '16.99', 'category': 'Pasta'},
        {'name': 'Tiramisu', 'description': 'Classic Italian dessert', 'price': '7.99', 'category': 'Dessert'}
    ]
    
    for item_data in pizza_items:
        MenuItem.objects.create(restaurant=restaurants[0], **item_data)
    
    # Burger Junction menu
    burger_items = [
        {'name': 'Classic Cheeseburger', 'description': 'Beef patty, cheese, lettuce, tomato, onion', 'price': '12.99', 'category': 'Burger'},
        {'name': 'BBQ Bacon Burger', 'description': 'Beef patty, bacon, BBQ sauce, onion rings', 'price': '15.99', 'category': 'Burger'},
        {'name': 'Veggie Burger', 'description': 'Plant-based patty, avocado, sprouts', 'price': '13.99', 'category': 'Burger'},
        {'name': 'French Fries', 'description': 'Crispy golden fries', 'price': '5.99', 'category': 'Side'},
        {'name': 'Onion Rings', 'description': 'Beer-battered onion rings', 'price': '6.99', 'category': 'Side'},
        {'name': 'Chocolate Shake', 'description': 'Rich chocolate milkshake', 'price': '6.99', 'category': 'Drink'},
        {'name': 'Vanilla Shake', 'description': 'Creamy vanilla milkshake', 'price': '6.99', 'category': 'Drink'},
        {'name': 'Buffalo Wings', 'description': 'Spicy chicken wings with ranch', 'price': '11.99', 'category': 'Appetizer'}
    ]
    
    for item_data in burger_items:
        MenuItem.objects.create(restaurant=restaurants[1], **item_data)
    
    # Sakura Sushi Bar menu
    sushi_items = [
        {'name': 'Salmon Roll', 'description': 'Fresh salmon with rice and nori', 'price': '8.99', 'category': 'Sushi'},
        {'name': 'California Roll', 'description': 'Crab, avocado, cucumber', 'price': '7.99', 'category': 'Sushi'},
        {'name': 'Tuna Roll', 'description': 'Fresh tuna with rice and nori', 'price': '9.99', 'category': 'Sushi'},
        {'name': 'Dragon Roll', 'description': 'Eel, cucumber, avocado on top', 'price': '14.99', 'category': 'Sushi'},
        {'name': 'Miso Soup', 'description': 'Traditional Japanese soup', 'price': '3.99', 'category': 'Soup'},
        {'name': 'Edamame', 'description': 'Steamed soybeans with sea salt', 'price': '5.99', 'category': 'Appetizer'},
        {'name': 'Chicken Teriyaki', 'description': 'Grilled chicken with teriyaki sauce', 'price': '16.99', 'category': 'Main'},
        {'name': 'Green Tea Ice Cream', 'description': 'Traditional Japanese dessert', 'price': '4.99', 'category': 'Dessert'}
    ]
    
    for item_data in sushi_items:
        MenuItem.objects.create(restaurant=restaurants[2], **item_data)
    
    # Taco Fiesta menu
    taco_items = [
        {'name': 'Beef Tacos (3)', 'description': 'Three soft tacos with seasoned beef', 'price': '9.99', 'category': 'Tacos'},
        {'name': 'Chicken Tacos (3)', 'description': 'Three soft tacos with grilled chicken', 'price': '10.99', 'category': 'Tacos'},
        {'name': 'Fish Tacos (3)', 'description': 'Three soft tacos with grilled fish', 'price': '12.99', 'category': 'Tacos'},
        {'name': 'Beef Burrito', 'description': 'Large flour tortilla with beef, rice, beans', 'price': '11.99', 'category': 'Burrito'},
        {'name': 'Chicken Quesadilla', 'description': 'Grilled tortilla with chicken and cheese', 'price': '9.99', 'category': 'Quesadilla'},
        {'name': 'Guacamole & Chips', 'description': 'Fresh guacamole with tortilla chips', 'price': '7.99', 'category': 'Appetizer'},
        {'name': 'Churros', 'description': 'Fried dough with cinnamon sugar', 'price': '6.99', 'category': 'Dessert'}
    ]
    
    for item_data in taco_items:
        MenuItem.objects.create(restaurant=restaurants[3], **item_data)
    
    # Golden Dragon menu
    chinese_items = [
        {'name': 'Sweet & Sour Pork', 'description': 'Crispy pork with sweet and sour sauce', 'price': '14.99', 'category': 'Main'},
        {'name': 'Kung Pao Chicken', 'description': 'Spicy chicken with peanuts', 'price': '13.99', 'category': 'Main'},
        {'name': 'Beef & Broccoli', 'description': 'Tender beef with fresh broccoli', 'price': '15.99', 'category': 'Main'},
        {'name': 'Fried Rice', 'description': 'Wok-fried rice with eggs and vegetables', 'price': '8.99', 'category': 'Rice'},
        {'name': 'Chow Mein', 'description': 'Stir-fried noodles with vegetables', 'price': '10.99', 'category': 'Noodles'},
        {'name': 'Spring Rolls (4)', 'description': 'Crispy vegetable spring rolls', 'price': '6.99', 'category': 'Appetizer'},
        {'name': 'Hot & Sour Soup', 'description': 'Traditional spicy and sour soup', 'price': '4.99', 'category': 'Soup'}
    ]
    
    for item_data in chinese_items:
        MenuItem.objects.create(restaurant=restaurants[4], **item_data)
    
    # Create sample orders
    print("Creating sample orders...")
    
    # Order 1 - Pizza order (in progress)
    order1 = Order.objects.create(
        restaurant=restaurants[0],
        customer_name="John Smith",
        status="in_progress",
        notes="Extra cheese on the pizza, please"
    )
    
    OrderItem.objects.create(
        order=order1,
        menu_item=MenuItem.objects.get(name="Margherita Pizza"),
        quantity=2,
        special_instructions="Extra cheese"
    )
    
    OrderItem.objects.create(
        order=order1,
        menu_item=MenuItem.objects.get(name="Caesar Salad"),
        quantity=1
    )
    
    OrderItem.objects.create(
        order=order1,
        menu_item=MenuItem.objects.get(name="Garlic Bread"),
        quantity=1
    )
    
    # Order 2 - Burger order (pending)
    order2 = Order.objects.create(
        restaurant=restaurants[1],
        customer_name="Jane Doe",
        status="pending",
        notes="No onions on the burger"
    )
    
    OrderItem.objects.create(
        order=order2,
        menu_item=MenuItem.objects.get(name="Classic Cheeseburger"),
        quantity=1,
        special_instructions="No onions"
    )
    
    OrderItem.objects.create(
        order=order2,
        menu_item=MenuItem.objects.get(name="French Fries"),
        quantity=1
    )
    
    OrderItem.objects.create(
        order=order2,
        menu_item=MenuItem.objects.get(name="Chocolate Shake"),
        quantity=1
    )
    
    # Order 3 - Sushi order (done)
    order3 = Order.objects.create(
        restaurant=restaurants[2],
        customer_name="Mike Johnson",
        status="done"
    )
    
    OrderItem.objects.create(
        order=order3,
        menu_item=MenuItem.objects.get(name="Salmon Roll"),
        quantity=2
    )
    
    OrderItem.objects.create(
        order=order3,
        menu_item=MenuItem.objects.get(name="California Roll"),
        quantity=1
    )
    
    OrderItem.objects.create(
        order=order3,
        menu_item=MenuItem.objects.get(name="Miso Soup"),
        quantity=1
    )
    
    # Order 4 - Taco order (pending)
    order4 = Order.objects.create(
        restaurant=restaurants[3],
        customer_name="Sarah Wilson",
        status="pending",
        notes="Make it spicy!"
    )
    
    OrderItem.objects.create(
        order=order4,
        menu_item=MenuItem.objects.get(name="Chicken Tacos (3)"),
        quantity=1,
        special_instructions="Extra spicy"
    )
    
    OrderItem.objects.create(
        order=order4,
        menu_item=MenuItem.objects.get(name="Guacamole & Chips"),
        quantity=1
    )
    
    # Order 5 - Chinese order (cancelled)
    order5 = Order.objects.create(
        restaurant=restaurants[4],
        customer_name="David Chen",
        status="cancelled",
        notes="Customer changed mind"
    )
    
    OrderItem.objects.create(
        order=order5,
        menu_item=MenuItem.objects.get(name="Kung Pao Chicken"),
        quantity=1
    )
    
    OrderItem.objects.create(
        order=order5,
        menu_item=MenuItem.objects.get(name="Fried Rice"),
        quantity=1
    )
    
    # Order 6 - Large pizza order (in progress)
    order6 = Order.objects.create(
        restaurant=restaurants[0],
        customer_name="Office Party",
        status="in_progress",
        notes="Corporate order - delivery to Suite 300"
    )
    
    OrderItem.objects.create(
        order=order6,
        menu_item=MenuItem.objects.get(name="Supreme Pizza"),
        quantity=3
    )
    
    OrderItem.objects.create(
        order=order6,
        menu_item=MenuItem.objects.get(name="Pepperoni Pizza"),
        quantity=2
    )
    
    OrderItem.objects.create(
        order=order6,
        menu_item=MenuItem.objects.get(name="Caesar Salad"),
        quantity=4
    )
    
    print(f"✅ Created {Restaurant.objects.count()} restaurants")
    print(f"✅ Created {MenuItem.objects.count()} menu items")
    print(f"✅ Created {Order.objects.count()} orders")
    print(f"✅ Created {OrderItem.objects.count()} order items")
    
    return True

def export_to_json():
    """Export all data to JSON file"""
    print("\nExporting data to JSON...")
    
    data = {
        'restaurants': [],
        'menu_items': [],
        'orders': [],
        'order_items': []
    }
    
    # Export restaurants
    for restaurant in Restaurant.objects.all():
        data['restaurants'].append({
            'id': restaurant.id,
            'name': restaurant.name,
            'description': restaurant.description,
            'is_active': restaurant.is_active,
            'created_at': restaurant.created_at.isoformat(),
            'updated_at': restaurant.updated_at.isoformat()
        })
    
    # Export menu items
    for menu_item in MenuItem.objects.all():
        data['menu_items'].append({
            'id': menu_item.id,
            'restaurant_id': menu_item.restaurant.id,
            'name': menu_item.name,
            'description': menu_item.description,
            'price': str(menu_item.price),
            'is_available': menu_item.is_available,
            'category': menu_item.category,
            'created_at': menu_item.created_at.isoformat(),
            'updated_at': menu_item.updated_at.isoformat()
        })
    
    # Export orders
    for order in Order.objects.all():
        data['orders'].append({
            'id': order.id,
            'restaurant_id': order.restaurant.id,
            'customer_name': order.customer_name,
            'status': order.status,
            'total_amount': str(order.total_amount),
            'notes': order.notes,
            'created_at': order.created_at.isoformat(),
            'updated_at': order.updated_at.isoformat()
        })
    
    # Export order items
    for order_item in OrderItem.objects.all():
        data['order_items'].append({
            'id': order_item.id,
            'order_id': order_item.order.id,
            'menu_item_id': order_item.menu_item.id,
            'quantity': order_item.quantity,
            'unit_price': str(order_item.unit_price),
            'subtotal': str(order_item.subtotal),
            'special_instructions': order_item.special_instructions
        })
    
    # Write to file
    with open('test_data_dump.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("✅ Data exported to test_data_dump.json")
    return True

if __name__ == "__main__":
    print("🚀 Generating comprehensive test data...")
    generate_test_data()
    export_to_json()
    print("\n🎉 Test data generation complete!") 