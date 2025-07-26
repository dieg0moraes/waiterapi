#!/usr/bin/env python
import os
import sys
import django
import json
from decimal import Decimal
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'waiterapi.settings')
django.setup()

from orders.models import Restaurant, MenuItem, Order, OrderItem
from django.contrib.auth.models import User
from django.utils import timezone

def clear_existing_data():
    """Clear all existing data from the database"""
    print("🗑️  Clearing existing data...")
    OrderItem.objects.all().delete()
    Order.objects.all().delete()
    MenuItem.objects.all().delete()
    Restaurant.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()
    print("✅ Existing data cleared")

def create_admin_user():
    """Create admin user if it doesn't exist"""
    print("👤 Creating admin user...")
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
        print("✅ Admin user created")
    else:
        print("ℹ️  Admin user already exists")

def load_data_from_json(filename='test_data_dump.json'):
    """Load test data from JSON dump file"""
    
    if not os.path.exists(filename):
        print(f"❌ Error: {filename} not found!")
        print(f"💡 Run 'python generate_test_data.py' first to create the dump file.")
        return False
    
    print(f"📁 Loading data from {filename}...")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error reading JSON file: {e}")
        return False
    except Exception as e:
        print(f"❌ Error opening file: {e}")
        return False
    
    # Create restaurants first
    print("🏪 Creating restaurants...")
    restaurant_id_map = {}  # Maps old IDs to new IDs
    
    for rest_data in data.get('restaurants', []):
        old_id = rest_data['id']
        restaurant = Restaurant.objects.create(
            name=rest_data['name'],
            description=rest_data['description'],
            is_active=rest_data['is_active']
        )
        restaurant_id_map[old_id] = restaurant.id
        print(f"  ✅ Created: {restaurant.name}")
    
    # Create menu items
    print("🍕 Creating menu items...")
    menu_item_id_map = {}  # Maps old IDs to new IDs
    
    for item_data in data.get('menu_items', []):
        old_id = item_data['id']
        old_restaurant_id = item_data['restaurant_id']
        new_restaurant_id = restaurant_id_map.get(old_restaurant_id)
        
        if new_restaurant_id is None:
            print(f"⚠️  Warning: Restaurant ID {old_restaurant_id} not found for menu item")
            continue
        
        try:
            restaurant = Restaurant.objects.get(id=new_restaurant_id)
            menu_item = MenuItem.objects.create(
                restaurant=restaurant,
                name=item_data['name'],
                description=item_data['description'],
                price=Decimal(item_data['price']),
                is_available=item_data['is_available'],
                category=item_data['category']
            )
            menu_item_id_map[old_id] = menu_item.id
            print(f"  ✅ Created: {menu_item.name} at {restaurant.name}")
        except Exception as e:
            print(f"❌ Error creating menu item {item_data['name']}: {e}")
            continue
    
    # Create orders
    print("📋 Creating orders...")
    order_id_map = {}  # Maps old IDs to new IDs
    
    for order_data in data.get('orders', []):
        old_id = order_data['id']
        old_restaurant_id = order_data['restaurant_id']
        new_restaurant_id = restaurant_id_map.get(old_restaurant_id)
        
        if new_restaurant_id is None:
            print(f"⚠️  Warning: Restaurant ID {old_restaurant_id} not found for order")
            continue
        
        try:
            restaurant = Restaurant.objects.get(id=new_restaurant_id)
            order = Order.objects.create(
                restaurant=restaurant,
                customer_name=order_data['customer_name'],
                status=order_data['status'],
                total_amount=Decimal(order_data['total_amount']),
                notes=order_data['notes']
            )
            order_id_map[old_id] = order.id
            print(f"  ✅ Created order for: {order.customer_name} at {restaurant.name}")
        except Exception as e:
            print(f"❌ Error creating order for {order_data['customer_name']}: {e}")
            continue
    
    # Create order items
    print("🛒 Creating order items...")
    
    for item_data in data.get('order_items', []):
        old_order_id = item_data['order_id']
        old_menu_item_id = item_data['menu_item_id']
        new_order_id = order_id_map.get(old_order_id)
        new_menu_item_id = menu_item_id_map.get(old_menu_item_id)
        
        if new_order_id is None:
            print(f"⚠️  Warning: Order ID {old_order_id} not found for order item")
            continue
        
        if new_menu_item_id is None:
            print(f"⚠️  Warning: Menu item ID {old_menu_item_id} not found for order item")
            continue
        
        try:
            order = Order.objects.get(id=new_order_id)
            menu_item = MenuItem.objects.get(id=new_menu_item_id)
            
            order_item = OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=item_data['quantity'],
                special_instructions=item_data['special_instructions']
            )
            print(f"  ✅ Added {menu_item.name} x{order_item.quantity} to order for {order.customer_name}")
        except Exception as e:
            print(f"❌ Error creating order item: {e}")
            continue
    
    # Update order totals
    print("💰 Updating order totals...")
    for order in Order.objects.all():
        order.calculate_total()
        order.save()
    
    return True

def print_summary():
    """Print a summary of loaded data"""
    print("\n📊 Data Loading Summary:")
    print(f"  🏪 Restaurants: {Restaurant.objects.count()}")
    print(f"  🍕 Menu Items: {MenuItem.objects.count()}")
    print(f"  📋 Orders: {Order.objects.count()}")
    print(f"  🛒 Order Items: {OrderItem.objects.count()}")
    
    print("\n🏪 Restaurants:")
    for restaurant in Restaurant.objects.all():
        status = "🟢 Active" if restaurant.is_active else "🔴 Inactive"
        print(f"  • {restaurant.name} ({status})")
    
    print("\n📋 Orders by Status:")
    for status, display in Order.STATUS_CHOICES:
        count = Order.objects.filter(status=status).count()
        if count > 0:
            print(f"  • {display}: {count}")

def main():
    """Main function to load test data"""
    print("🚀 Loading Test Data from JSON Dump")
    print("=" * 50)
    
    # Check if we should clear existing data
    if len(sys.argv) > 1 and sys.argv[1] == '--keep-existing':
        print("ℹ️  Keeping existing data (--keep-existing flag detected)")
    else:
        clear_existing_data()
    
    # Create admin user
    create_admin_user()
    
    # Load data from JSON
    filename = 'test_data_dump.json'
    if len(sys.argv) > 1 and not sys.argv[1].startswith('--'):
        filename = sys.argv[1]
    
    success = load_data_from_json(filename)
    
    if success:
        print_summary()
        print("\n🎉 Test data loaded successfully!")
        print("\n💡 You can now:")
        print("   • Visit http://localhost:8000/api/ to explore the API")
        print("   • Login to admin at http://localhost:8000/admin/ (admin/admin123)")
        print("   • Test endpoints with the Postman collection")
    else:
        print("\n❌ Failed to load test data")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 