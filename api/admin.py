from django.contrib import admin

from .models import ShoppingListItem, InventoryItem

admin.site.register(ShoppingListItem)
admin.site.register(InventoryItem)
