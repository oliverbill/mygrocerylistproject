from datetime import datetime

from django.db import models
from django.db.models import DateTimeField, CharField, \
    DecimalField, IntegerField, PositiveSmallIntegerField

current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
str_current_datetime = str(current_datetime)

GROCERY_STORES = [("A", "AUDI"), ("C", "CONTINENTE"), ("L", "LIDL"), ("P", "PINGO DOCE"), ("I", "INTERMARCHE"),
                  ("O", "OUTRO")]

class ShoppingListItem(models.Model):
    created = DateTimeField(auto_now_add=True)
    item_name = CharField(max_length=100)
    item_quantity = PositiveSmallIntegerField(default=1)
    item_brand = CharField(null=True, max_length=50)
    item_grocery_store = CharField(choices=GROCERY_STORES, max_length=15)
    expected_item_price_max = DecimalField(decimal_places=2, max_digits=10)
    creator = models.ForeignKey(
        "auth.User", related_name="shoppinglistitems", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['created']

class InventoryItem(models.Model):
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    name = CharField(max_length=50)
    brand = CharField(max_length=100)
    grocery_store = CharField(null=True, choices=GROCERY_STORES, max_length=15)
    quantity = PositiveSmallIntegerField(null=True)
    payed_price = DecimalField(null=True, decimal_places=2, max_digits=10)
    # calculated fields
    min_alert = PositiveSmallIntegerField(default=1)
    stockout_at = DateTimeField(null=True, blank=True)

    shoppinglistitem = models.OneToOneField(ShoppingListItem, on_delete=models.CASCADE)

    creator = models.ForeignKey(
        "auth.User", related_name="shoppinglistitem", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['updated']

