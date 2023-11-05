import os
from http import HTTPStatus

import pytest
from _decimal import Decimal
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from api.models import InventoryItem, ShoppingListItem


class ShoppingListItemE2ETest(APITestCase):

    def setUp(self):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mygrocerylistapp.settings')
        self.client = APIClient()
        self.user = User.objects.create_superuser(
            username='admin',
            password='admin',
            email='admin@test.com'
        )
        self.client.force_authenticate(user=self.user)
        self.base_url = reverse('shoppinglistitem-list')
        self.shoppinglistitem = {
            'item_name': 'chocolate',
            'item_quantity': '3',
            'item_brand': 'Lindt',
            'item_grocery_store': 'A',
            'expected_item_price_max': '4.12',
            'creator': 'http://127.0.0.1:8000/users/1/'
        }

    @pytest.mark.django_db
    def test_post(self):
        response = self.client.post(self.base_url, data=self.shoppinglistitem, format='json')
        self.assertEqual(response.status_code, HTTPStatus.CREATED._value_)

        self.assertEqual(ShoppingListItem.objects.get().item_name, self.shoppinglistitem['item_name'])
        self.assertEqual(ShoppingListItem.objects.get().item_brand, self.shoppinglistitem['item_brand'])
        self.assertEqual(ShoppingListItem.objects.get().item_quantity, int(self.shoppinglistitem['item_quantity']))
        self.assertEqual(ShoppingListItem.objects.get().item_grocery_store, self.shoppinglistitem['item_grocery_store'])
        self.assertEqual(ShoppingListItem.objects.get().expected_item_price_max,
                         Decimal(self.shoppinglistitem['expected_item_price_max']))

        response = self.client.get(self.shoppinglistitem['creator'], format='json')
        self.assertEqual(response.status_code, HTTPStatus.OK._value_)
        self.assertEqual(ShoppingListItem.objects.get().creator.username, response.data['username'])

        self.assert_inventory_item_is_created(self.shoppinglistitem, response.data['username'])

    def assert_inventory_item_is_created(self, shoppinglistitem, username):
        self.assertEqual(InventoryItem.objects.get().name, shoppinglistitem['item_name'])
        self.assertEqual(InventoryItem.objects.get().quantity, int(shoppinglistitem['item_quantity']))
        self.assertEqual(InventoryItem.objects.get().brand, shoppinglistitem['item_brand'])
        self.assertEqual(InventoryItem.objects.get().grocery_store, shoppinglistitem['item_grocery_store'])
        self.assertEqual(InventoryItem.objects.get().creator.username, username)

    @pytest.mark.django_db
    def test_get(self):
        # post test data
        self.client.post(self.base_url, data=self.shoppinglistitem, format='json')
        # get posted test data
        response = self.client.get(path=self.base_url, format='json')
        results = response.data['results'][0]
        self.assertEqual(results['item_name'], self.shoppinglistitem['item_name'])
        self.assertEqual(results['item_brand'], self.shoppinglistitem['item_brand'])
        self.assertEqual(results['item_quantity'], int(self.shoppinglistitem['item_quantity']))
        self.assertEqual(results['item_grocery_store'], self.shoppinglistitem['item_grocery_store'])
        self.assertEqual(results['expected_item_price_max'], self.shoppinglistitem['expected_item_price_max'])

        self.assertEqual(ShoppingListItem.objects.count(), 1)

    @pytest.mark.django_db
    def test_patch(self):
        # post test data
        response = self.client.post(self.base_url, data=self.shoppinglistitem, format='json')
        self.assertEqual(response.status_code, HTTPStatus.CREATED._value_)
        #
        self.assertEqual(ShoppingListItem.objects.count(), 1)
        posted_item = ShoppingListItem.objects.get()
        response = self.client.patch(path=f'{self.base_url}{posted_item.id}/',
                                     data={'item_brand': 'Continente'},
                                     format='json')
        self.assertEqual(response.status_code, HTTPStatus.OK._value_)
        self.assertEqual(ShoppingListItem.objects.get(pk=1).item_brand, 'Continente')

    @pytest.mark.django_db
    def test_put(self):
        # post test data
        response = self.client.post(self.base_url, data=self.shoppinglistitem, format='json')
        self.assertEqual(response.status_code, HTTPStatus.CREATED._value_)
        #
        self.assertEqual(ShoppingListItem.objects.count(), 1)
        posted_item = ShoppingListItem.objects.get()
        response = self.client.put(path=f'{self.base_url}{posted_item.id}/',
                                   ## PUT tem q passar todos os fields, senao da HTTP 400: campo c preenchimento obrigatorio
                                   data={
                                       'item_name': self.shoppinglistitem['item_name'],
                                       'item_quantity': self.shoppinglistitem['item_quantity'],
                                       'item_brand': 'Continente',
                                       'item_grocery_store': self.shoppinglistitem['item_grocery_store'],
                                       'expected_item_price_max': self.shoppinglistitem['expected_item_price_max'],
                                       'creator': self.shoppinglistitem['creator']
                                   },
                                   format='json')

        self.assertEqual(response.status_code, HTTPStatus.OK._value_)
        self.assertEqual(ShoppingListItem.objects.get(pk=1).item_brand, 'Continente')

