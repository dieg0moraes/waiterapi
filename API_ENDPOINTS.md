# Waiter API - Restaurant Order Management System

A Django REST API for managing restaurant orders in a food court setting.

## Base URL
```
http://localhost:8000/api/
```

## Authentication
Currently set to allow anonymous access for development. Production deployments should implement proper authentication.

## Available Endpoints

### Restaurants

#### List all restaurants
- **GET** `/api/restaurants/`
- **Query Parameters:**
  - `is_active`: Filter by active status (true/false)
  - `search`: Search by name or description
  - `ordering`: Sort by name, created_at

#### Get specific restaurant
- **GET** `/api/restaurants/{id}/`

#### Create restaurant
- **POST** `/api/restaurants/`
```json
{
  "name": "Restaurant Name",
  "description": "Restaurant description",
  "is_active": true
}
```

#### Update restaurant
- **PUT/PATCH** `/api/restaurants/{id}/`

#### Delete restaurant
- **DELETE** `/api/restaurants/{id}/`

#### Get restaurant menu
- **GET** `/api/restaurants/{id}/menu/`
- Returns all available menu items for the restaurant

#### Get restaurant orders
- **GET** `/api/restaurants/{id}/orders/`
- **Query Parameters:**
  - `status`: Filter by order status (pending, in_progress, done, cancelled)

### Menu Items

#### List menu items
- **GET** `/api/menu-items/`
- **Query Parameters:**
  - `restaurant`: Filter by restaurant ID
  - `is_available`: Filter by availability (true/false)
  - `category`: Filter by category
  - `search`: Search by name or description
  - `ordering`: Sort by name, price, created_at

#### Get specific menu item
- **GET** `/api/menu-items/{id}/`

#### Create menu item
- **POST** `/api/menu-items/`
```json
{
  "restaurant": 1,
  "name": "Item Name",
  "description": "Item description",
  "price": "10.99",
  "category": "Main",
  "is_available": true
}
```

#### Update menu item
- **PUT/PATCH** `/api/menu-items/{id}/`

#### Delete menu item
- **DELETE** `/api/menu-items/{id}/`

### Orders

#### List orders
- **GET** `/api/orders/`
- **Query Parameters:**
  - `restaurant`: Filter by restaurant ID
  - `status`: Filter by status
  - `search`: Search by customer name
  - `ordering`: Sort by created_at, updated_at, total_amount

#### Get specific order
- **GET** `/api/orders/{id}/`

#### Create order
- **POST** `/api/orders/`
```json
{
  "restaurant": 1,
  "customer_name": "John Doe",
  "notes": "Special instructions",
  "order_items": [
    {
      "menu_item": 1,
      "quantity": 2,
      "special_instructions": "No onions"
    },
    {
      "menu_item": 3,
      "quantity": 1
    }
  ]
}
```

#### Update order status
- **PATCH** `/api/orders/{id}/update_status/`
```json
{
  "status": "in_progress"
}
```

**Status Transitions:**
- `pending` → `in_progress` or `cancelled`
- `in_progress` → `done` or `cancelled`
- `done` → (no transitions)
- `cancelled` → (no transitions)

#### Get orders by restaurant
- **GET** `/api/orders/by_restaurant/?restaurant_id={restaurant_id}`
- **Query Parameters:**
  - `restaurant_id`: Required - Restaurant ID
  - `status`: Optional - Filter by status

#### Get order statistics
- **GET** `/api/orders/statistics/`
- **Query Parameters:**
  - `restaurant_id`: Optional - Filter statistics by restaurant
- **Returns:**
```json
{
  "total_orders": 10,
  "pending_orders": 3,
  "in_progress_orders": 2,
  "done_orders": 4,
  "cancelled_orders": 1,
  "total_revenue": "150.45"
}
```

## Example Usage

### Create a new order
```bash
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "restaurant": 1,
    "customer_name": "Alice Brown",
    "notes": "Table 5",
    "order_items": [
      {
        "menu_item": 1,
        "quantity": 1,
        "special_instructions": "Extra crispy"
      },
      {
        "menu_item": 2,
        "quantity": 2
      }
    ]
  }'
```

### Update order status
```bash
curl -X PATCH http://localhost:8000/api/orders/1/update_status/ \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress"}'
```

### Get all orders for a restaurant
```bash
curl http://localhost:8000/api/orders/by_restaurant/?restaurant_id=1
```

### Get pending orders for a restaurant
```bash
curl http://localhost:8000/api/orders/by_restaurant/?restaurant_id=1&status=pending
```

## Response Format

### Successful Response
```json
{
  "id": 1,
  "restaurant": 1,
  "restaurant_name": "Mario's Pizza",
  "customer_name": "John Doe",
  "status": "pending",
  "status_display": "Pending",
  "total_amount": "25.98",
  "notes": "Extra cheese please",
  "order_items": [
    {
      "id": 1,
      "menu_item": 1,
      "menu_item_name": "Margherita Pizza",
      "menu_item_description": "Fresh tomato sauce, mozzarella, and basil",
      "quantity": 1,
      "unit_price": "15.99",
      "subtotal": "15.99",
      "special_instructions": ""
    }
  ],
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Error Response
```json
{
  "error": "Error message",
  "details": {
    "field_name": ["Error description"]
  }
}
```

## Admin Interface

Access the Django admin interface at:
```
http://localhost:8000/admin/
```

Use the superuser credentials created during setup to manage data through the web interface.

## Sample Data

The system comes with sample data including:
- 3 restaurants (Mario's Pizza, Burger Palace, Sakura Sushi)
- 9 menu items across different categories
- 3 sample orders in different statuses

## Development Notes

- The API uses pagination with 20 items per page by default
- All timestamps are in UTC
- Prices are stored as decimal values with 2 decimal places
- Order totals are automatically calculated when order items are added/modified
- Menu items must belong to the same restaurant when creating orders 