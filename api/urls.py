from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'inventoryitem', views.InventoryItemViewSet, basename="inventoryitem")
router.register(r'shoppinglistitem', views.ShoppingListItemViewSet, basename="shoppinglistitem")
router.register(r'users', views.UserViewSet, basename="user")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]

