from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Category, Product
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


User = get_user_model()

class TestProducts(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email='test@test.com',
            password='qwert1234',
            name='testuser',
            is_active=True

        )
        self.admin = User.objects.create_superuser(
            email='admin@admin.com',
            password='12345qwerty',
            name='admin',

        )
        self.user1_token = get_tokens_for_user(self.user1)
        self.admin_token = get_tokens_for_user(self.admin)
        self.category = Category.objects.create(name='compy', slug='compy')
        self.products1 = Product.objects.create(
            name='lola',
            description='Lola is not Bola',
            category=self.category,
            price=1000
        )
        self.products2 = Product.objects.create(
            name='Car',
            description='AUDI',
            category=self.category,
            price=4500
        )
        self.products3 = Product.objects.create(
            name='Torro',
            description='Torro Torro',
            category=self.category,
            price=1200
        )
        self.products4 = Product.objects.create(
            name='Invoker',
            description='Meteor',
            category=self.category,
            price=7200
        )
        self.products5 = Product.objects.create(
            name='Nsaf',
            description='agsa',
            category=self.category,
            price=10
        )
        self.product_payload = {
            'name': 'SegaMegaDrive',
            'description': 'Ho-Ho-Ho',
            'category': self.category.id,
            'price': 2000
        }

    def test_create_products_as_anonymous_user(self):
        data = self.product_payload.copy()
        client = APIClient()
        url = 'http://localhost/products/'
        respons = client.post(url, data)
        self.assertEqual(respons.status_code, 401)

    
    def test_create_product_as_user(self):
        data = self.product_payload.copy()
        client = APIClient()
        url = 'http://localhost/products/'
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user1_token.get("access")}')
        respons = client.post(url, data)
        self.assertEqual(respons.status_code, 403)


    def test_create_product_as_superuser(self):
        data = self.product_payload.copy()
        client = APIClient()
        url = 'http://localhost/products/'
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.get("access")}')
        respons = client.post(url, data)
        self.assertEqual(respons.status_code, 201)
