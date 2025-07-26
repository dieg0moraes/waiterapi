from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'restaurants', views.RestaurantViewSet)
router.register(r'menu-items', views.MenuItemViewSet)
router.register(r'orders', views.OrderViewSet)

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('api/', include(router.urls)),
] 