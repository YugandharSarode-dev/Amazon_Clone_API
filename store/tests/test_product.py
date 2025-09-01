from django.test import TestCase
import random
from utility.constants import BASE_URL
from utility.test_utility import *
from stark_utilities.utilities import random_string_generator
from ..models import Product

class ProductTest(TestCase):
    model_class = Product

    @classmethod
    def setUpTestData(cls):
        cls.superuser = create_user(SUPERUSER_ROLE)
        cls.auth_headers = get_auth_dict(cls.superuser)
        cls.superuser.set_password("reset123")
        cls.superuser.save()
        cls.get_instance, created = cls.model_class.objects.get_or_create(id=1, name="DefaultProduct")

    url = BASE_URL + 'product/'
    data = dict()

    def test_add_api_valid(self):
        self.data['name'] = random_string_generator()
        self.data['description'] = "Test Description"
        self.data['price'] = 100
        self.data['stock'] = 10
        self.data['category'] = 1
        response = self.client.post(self.url, data=self.data, **self.auth_headers)
        self.assertEqual(response.status_code, 201)

    def test_add_api_empty(self):
        self.data = dict()
        response = self.client.post(self.url, data=self.data, **self.auth_headers)
        self.assertEqual(response.status_code, 400)

    def test_put_api_valid(self):
        self.data['id'] = self.get_instance.id
        self.data['price'] = 200
        response = self.client.put(self.url, data=self.data, **self.auth_headers)
        self.assertEqual(response.status_code, 200)

    def test_put_api_invalid(self):
        self.data['id'] = 999999
        self.data['price'] = 200
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
