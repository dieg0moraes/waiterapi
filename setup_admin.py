#!/usr/bin/env python
import os
import sys
import subprocess

# Import the load_test_data script
from load_test_data import main as load_main

def setup_admin_and_data():
    """Setup admin user and load comprehensive test data"""
    print("🚀 Setting up admin user and loading test data...")
    
    # Import Django to check if data exists
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'waiterapi.settings')
    django.setup()
    
    from orders.models import Restaurant
    
    # Check if data already exists
    data_exists = Restaurant.objects.exists()
    
    
    # Check if dump file exists, if not generate it
    if not os.path.exists('test_data_dump.json'):
        print("📦 Test data dump not found, generating...")
        try:
            result = subprocess.run([sys.executable, 'generate_test_data.py'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Error generating test data: {result.stderr}")
                return False
            print("✅ Test data generated successfully")
        except Exception as e:
            print(f"❌ Error running generate_test_data.py: {e}")
            return False
    
    # Load the test data using the load_test_data script
    try:
        # Don't pass any flags - will clear existing and load fresh
        original_argv = sys.argv.copy()
        sys.argv = ['load_test_data.py']
        
        result = load_main()
        
        # Restore original argv
        sys.argv = original_argv
        
        return result == 0
    except Exception as e:
        print(f"❌ Error loading test data: {e}")
        return False

if __name__ == "__main__":
    success = setup_admin_and_data()
    if not success:
        sys.exit(1) 