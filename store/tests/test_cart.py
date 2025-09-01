from site import USER_SITE
from django.test import TestCase
import random
from utility.constants import BASE_URL
from utility.test_utility import *
from stark_utilities.utilities import random_string_generator
from ..models import Cart, Product

class CartTest(TestCase):
    model_class = Cart

    @classmethod
    def setUpTestData(cls):
        cls.user = create_user(USER_SITE)
        cls.auth_headers = get_auth_dict(cls.user)
        cls.user.set_password("reset123")
        cls.user.save()

        cls.product, _ = Product.objects.get_or_create(id=1, name="DefaultProduct", price=100, stock=10, category_id=1)
        cls.get_instance, created = cls.model_class.objects.get_or_create(id=1, user=cls.user, product=cls.product, quantity=1)

    url = BASE_URL + 'cart/'
    data = dict()

    def test_add_api_valid(self):
        self.data['product'] = self.product.id
        self.data['quantity'] = 2
        response = self.client.post(self.url, data=self.data, **self.auth_headers)
        self.assertEqual(response.status_code, 201)

    def test_add_api_empty(self):
        self.data = dict()
        response = self.client.post(self.url, data=self.data, **self.auth_headers)
        self.assertEqual(response.status_code, 400)

    def test_put_api_valid(self):
        self.data['id'] = self.get_instance.id
        self.data['quantity'] = 5
        response = self.client.put(self.url, data=self.data, **self.auth_headers)
        self.assertEqual(response.status_code, 200)

    def test_put_api_invalid(self):
        self.data['id'] = 999999
        self.data['quantity'] = 5
        response = self.client.put(self.url, data=self.data, **self.auth_headers)
        self.assertEqual(response.status_code, 404)

    def test_get_api_valid(self):
        response = self.client.get(self.url, **self.auth_headers)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_api_valid(self):
        url = self.url + str(self.get_instance.id) + '/'
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_api_invalid(self):
        url = self.url + '50000/'
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, 404)

    def test_del_api_valid(self):
        url = self.url + str(self.get_instance.id) + '/'
        response = self.client.delete(url, **self.auth_headers)
        self.assertEqual(response.status_code, 200)

    def test_del_api_invalid(self):
        url = self.url + '5000000/'
        response = self.client.delete(url, **self.auth_headers)
        self.assertEqual(response.status_code, 404)
