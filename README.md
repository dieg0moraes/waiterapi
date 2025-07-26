# Waiter API - Restaurant Order Management System

A Django REST API for managing restaurant orders in a food court setting. This system allows multiple restaurants to manage their menus and process orders through a unified API interface.

## Features

- ✅ Multi-restaurant support
- ✅ Menu management per restaurant
- ✅ Order creation and tracking
- ✅ Order status management (pending → in_progress → done)
- ✅ Automatic order total calculation
- ✅ RESTful API with filtering and search
- ✅ Django admin interface
- ✅ Docker support

## Quick Start with Docker

### Prerequisites
- Docker and Docker Compose installed

### Run with Docker Compose
```bash
# Clone the repository
git clone <repository-url>
cd waiterapi

# Build and start the application
docker-compose up --build

# The API will be available at http://localhost:8000
```

### Admin Access
- **URL:** http://localhost:8000/admin/
- **Username:** `admin`
- **Password:** `admin123`

### API Documentation
- **Base URL:** http://localhost:8000/api/
- **Browsable API:** http://localhost:8000/api/ (with Django REST Framework interface)

## Local Development Setup

### Prerequisites
- Python 3.12+
- virtualenv or similar

### Installation
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data
python setup_admin.py

# Start development server
python manage.py runserver
```

## API Endpoints

### Restaurants
- `GET /api/restaurants/` - List all restaurants
- `POST /api/restaurants/` - Create restaurant
- `GET /api/restaurants/{id}/` - Get restaurant details
- `GET /api/restaurants/{id}/menu/` - Get restaurant menu
- `GET /api/restaurants/{id}/orders/` - Get restaurant orders

### Menu Items
- `GET /api/menu-items/` - List menu items
- `POST /api/menu-items/` - Create menu item
- `GET /api/menu-items/{id}/` - Get menu item details

### Orders
- `GET /api/orders/` - List orders
- `POST /api/orders/` - Create order
- `GET /api/orders/{id}/` - Get order details
- `PATCH /api/orders/{id}/update_status/` - Update order status
- `GET /api/orders/by_restaurant/?restaurant_id={id}` - Get orders by restaurant
- `GET /api/orders/statistics/` - Get order statistics

## Example API Usage

### Create an Order
```bash
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "restaurant": 1,
    "customer_name": "John Doe",
    "notes": "Table 5",
    "order_items": [
      {
        "menu_item": 1,
        "quantity": 2,
        "special_instructions": "Extra cheese"
      },
      {
        "menu_item": 2,
        "quantity": 1
      }
    ]
  }'
```

### Update Order Status
```bash
curl -X PATCH http://localhost:8000/api/orders/1/update_status/ \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress"}'
```

### Get Restaurant Orders
```bash
curl "http://localhost:8000/api/orders/by_restaurant/?restaurant_id=1&status=pending"
```

## Order Status Flow

```
pending → in_progress → done
    ↓           ↓
cancelled   cancelled
```

## Sample Data

The system includes sample data with:
- 3 restaurants (Mario's Pizza, Burger Palace, Sakura Sushi)
- 9 menu items across different categories
- Sample orders in various statuses

## Docker Commands

```bash
# Build the image
docker build -t waiterapi .

# Run the container
docker run -p 8000:8000 waiterapi

# Use docker-compose for development
docker-compose up

# View logs
docker-compose logs waiterapi

# Stop the application
docker-compose down
```

## Development

### Project Structure
```
waiterapi/
├── waiterapi/           # Django project settings
├── orders/              # Main application
│   ├── models.py        # Database models
│   ├── views.py         # API views
│   ├── serializers.py   # DRF serializers
│   ├── urls.py          # URL routing
│   └── admin.py         # Admin interface
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose setup
└── API_ENDPOINTS.md    # Detailed API documentation
```

### Key Models
- **Restaurant**: Food court restaurants
- **MenuItem**: Menu items with pricing and categories
- **Order**: Customer orders with status tracking
- **OrderItem**: Individual items within orders

## Environment Variables

When deploying, you can set these environment variables:
- `DEBUG`: Set to `0` for production
- `SECRET_KEY`: Django secret key
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License. 