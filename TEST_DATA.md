# Test Data Management

This project includes a comprehensive test data management system with scripts to generate, export, and load test data for development and testing purposes.

## 📁 Files Overview

- **`generate_test_data.py`** - Generates comprehensive test data and exports to JSON
- **`load_test_data.py`** - Loads test data from JSON dump file
- **`test_data_dump.json`** - JSON file containing all test data (auto-generated)
- **`setup_admin.py`** - Docker setup script (uses load_test_data.py)

## 🚀 Usage

### Generate Test Data
Creates comprehensive test data and exports it to `test_data_dump.json`:

```bash
python generate_test_data.py
```

This will create:
- ✅ **6 restaurants** (5 active, 1 inactive)
- ✅ **38 menu items** across different categories
- ✅ **6 sample orders** in various statuses
- ✅ **16 order items** with different quantities
- ✅ **Admin user** (username: admin, password: admin123)

### Load Test Data
Loads test data from the JSON dump file:

```bash
# Clear existing data and load from dump
python load_test_data.py

# Keep existing data and add from dump
python load_test_data.py --keep-existing

# Load from specific file
python load_test_data.py custom_dump.json
```

### Quick Setup (Docker/Production)
The `setup_admin.py` script automatically handles everything:

```bash
python setup_admin.py
```

This script:
1. Checks if `test_data_dump.json` exists
2. If not, runs `generate_test_data.py` to create it
3. Loads the data using `load_test_data.py`

## 📊 Generated Test Data

### Restaurants
1. **Mario's Pizza Palace** - Italian cuisine with pizzas and pasta
2. **Burger Junction** - American burgers and sides
3. **Sakura Sushi Bar** - Japanese sushi and dishes
4. **Taco Fiesta** - Mexican tacos and burritos
5. **Golden Dragon** - Chinese dishes and dim sum
6. **Pasta Corner** - Italian pasta (inactive/closed)

### Menu Categories
- **Pizza** (4 varieties)
- **Burgers** (3 types)
- **Sushi** (4 types)
- **Tacos & Burritos** (5 options)
- **Chinese Mains** (3 dishes)
- **Sides & Appetizers** (8 items)
- **Soups** (2 options)
- **Desserts** (3 options)
- **Drinks** (2 shakes)

### Sample Orders
- **Pending Orders** (2) - New orders waiting to be processed
- **In Progress Orders** (2) - Orders currently being prepared
- **Completed Orders** (1) - Finished orders
- **Cancelled Orders** (1) - Orders that were cancelled

## 🔧 Script Features

### `generate_test_data.py`
- Clears existing data before generating new data
- Creates realistic restaurant menus with proper categorization
- Generates diverse orders with different statuses
- Exports everything to JSON with proper ID mapping
- Creates admin user automatically

### `load_test_data.py`
- Handles ID mapping when loading (old IDs → new IDs)
- Validates data integrity during import
- Provides detailed progress feedback
- Option to keep or clear existing data
- Calculates order totals automatically
- Shows comprehensive summary after loading

## 🐳 Docker Integration

The test data system is integrated into the Docker setup:

1. **Dockerfile** includes the test data scripts
2. **start.sh** runs `setup_admin.py` during container startup
3. **docker-compose.yml** mounts the data directory properly

When you run `docker-compose up`, the container will:
1. Run migrations
2. Generate test data (if needed)
3. Load test data
4. Start the Django server

## 🔄 Development Workflow

### Local Development
```bash
# Set up fresh environment
python manage.py migrate
python generate_test_data.py

# Reset data during development
python load_test_data.py

# Add more test scenarios
# Edit generate_test_data.py to add new data
python generate_test_data.py
```

### Testing/CI
```bash
# Quick setup for testing
python setup_admin.py

# Or use existing dump
python load_test_data.py existing_dump.json
```

## 📋 Data Structure

The JSON dump file contains four main sections:

```json
{
  "restaurants": [...],
  "menu_items": [...],
  "orders": [...],
  "order_items": [...]
}
```

Each section includes all necessary fields with proper relationships maintained through ID mapping during load.

## ⚡ Performance

- **Generation**: ~0.5 seconds for full dataset
- **Loading**: ~0.3 seconds for full dataset
- **File Size**: ~19KB for complete test data
- **Memory**: Minimal memory footprint

## 🔍 Troubleshooting

### "no such table" error
Run migrations first:
```bash
python manage.py migrate
```

### JSON file not found
Generate it first:
```bash
python generate_test_data.py
```

### Permission errors
Make sure scripts are executable:
```bash
chmod +x generate_test_data.py load_test_data.py
```

## 🎯 Best Practices

1. **Always run migrations** before generating test data
2. **Use `--keep-existing`** when you want to preserve data
3. **Generate fresh data** for clean testing environments
4. **Backup important data** before running scripts
5. **Check logs** for any warnings during data loading 