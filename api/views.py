from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from api.models import ShoppingListItem, InventoryItem
from api.serializers import UserSerializer, ShoppingListItemSerializer, \
    InventoryItemSerializer


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "users": reverse("user-list", request=request, format=format),
            "shoppinglistitems": reverse("shoppinglistitem-list", request=request, format=format),
            "inventoryitems": reverse("inventoryitem-list", request=request, format=format),
        }
    )

class InventoryItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class ShoppingListItemViewSet(viewsets.ModelViewSet):
    queryset = ShoppingListItem.objects.all()
    serializer_class = ShoppingListItemSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        if serializer.is_valid():
            newshoppinglistitem = serializer.save(creator=self.request.user)

            inv = InventoryItem(creator=self.request.user, name=newshoppinglistitem.item_name,
                                brand=newshoppinglistitem.item_brand,
                                grocery_store=newshoppinglistitem.item_grocery_store,
                                quantity=newshoppinglistitem.item_quantity, shoppinglistitem=newshoppinglistitem)
            InventoryItem.save(inv)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
