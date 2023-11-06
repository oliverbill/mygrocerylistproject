from django.contrib.auth.models import User
from rest_framework import permissions, viewsets, mixins, status
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

class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request):
        response = {'message': 'POST method is not allowed.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        response = {'message': 'DELETE method is not allowed.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

class ShoppingListItemViewSet(viewsets.ModelViewSet):
    queryset = ShoppingListItem.objects.all()
    serializer_class = ShoppingListItemSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        if serializer.is_valid():
            newshoppinglistitem = serializer.save(buyer=self.request.user)

            inv = InventoryItem(creator=self.request.user, name=newshoppinglistitem.item_name,
                                brand=newshoppinglistitem.item_brand,
                                grocery_store=newshoppinglistitem.item_grocery_store,
                                quantity=newshoppinglistitem.item_quantity, shoppinglistitem=newshoppinglistitem)
            InventoryItem.save(inv)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
