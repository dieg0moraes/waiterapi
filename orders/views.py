from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Restaurant, MenuItem, Order, OrderItem
from .serializers import (
    RestaurantSerializer, MenuItemSerializer, OrderSerializer,
    OrderCreateSerializer, OrderStatusUpdateSerializer
)


class RestaurantViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing restaurants
    Provides CRUD operations for restaurants
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def menu(self, request, pk=None):
        """Get menu items for a specific restaurant"""
        restaurant = self.get_object()
        menu_items = MenuItem.objects.filter(restaurant=restaurant, is_available=True)
        serializer = MenuItemSerializer(menu_items, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def orders(self, request, pk=None):
        """Get orders for a specific restaurant"""
        restaurant = self.get_object()
        orders = Order.objects.filter(restaurant=restaurant)
        
        # Filter by status if provided
        status_filter = request.query_params.get('status')
        if status_filter:
            orders = orders.filter(status=status_filter)
        
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class MenuItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing menu items
    Provides CRUD operations for menu items
    """
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['restaurant', 'is_available', 'category']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['restaurant', 'category', 'name']


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing orders
    Provides comprehensive order management functionality
    """
    queryset = Order.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['restaurant', 'status']
    search_fields = ['customer_name']
    ordering_fields = ['created_at', 'updated_at', 'total_amount']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action == 'update_status':
            return OrderStatusUpdateSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        """Create a new order with order items"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        # Return the created order with full details
        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Update only the status of an order"""
        order = self.get_object()
        serializer = OrderStatusUpdateSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # Return the updated order with full details
        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data)

    @action(detail=False, methods=['get'])
    def by_restaurant(self, request):
        """Get orders filtered by restaurant"""
        restaurant_id = request.query_params.get('restaurant_id')
        if not restaurant_id:
            return Response(
                {'error': 'restaurant_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        orders = Order.objects.filter(restaurant=restaurant)
        
        # Apply additional filters
        status_filter = request.query_params.get('status')
        if status_filter:
            orders = orders.filter(status=status_filter)
        
        # Paginate the results
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = OrderSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get order statistics"""
        restaurant_id = request.query_params.get('restaurant_id')
        queryset = self.get_queryset()
        
        if restaurant_id:
            queryset = queryset.filter(restaurant_id=restaurant_id)
        
        total_orders = queryset.count()
        pending_orders = queryset.filter(status='pending').count()
        in_progress_orders = queryset.filter(status='in_progress').count()
        done_orders = queryset.filter(status='done').count()
        cancelled_orders = queryset.filter(status='cancelled').count()
        
        # Calculate total revenue from completed orders
        total_revenue = sum(
            order.total_amount for order in queryset.filter(status='done')
        )
        
        return Response({
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'in_progress_orders': in_progress_orders,
            'done_orders': done_orders,
            'cancelled_orders': cancelled_orders,
            'total_revenue': str(total_revenue),
        })
