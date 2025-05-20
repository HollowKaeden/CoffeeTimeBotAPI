import random
import string
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from api.models import Coffee, Addon, TelegramUser


class CoffeeTimeAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = TelegramUser.objects.create(
            telegram_id="123456", first_name="Test", username="tester"
        )

        self.coffee = Coffee.objects.create(name="Латте", price=200)
        self.addon1 = Addon.objects.create(name="Сироп", price=30)
        self.addon2 = Addon.objects.create(name="Молоко", price=20)

    def test_coffee_list(self):
        response = self.client.get(reverse('coffee-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Латте', str(response.data))

    def test_invalid_token_returns_401(self):
        # Подставляем фейковый токен
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer invalid.token.value')

        data = {
            "items": [
                {
                    "coffee": self.coffee.id,
                    "addons": [self.addon1.id]
                }
            ]
        }
        response = self.client.post(reverse('create-order'), data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_access(self):
        response = self.client.get(reverse('user-orders'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def generate_random_value(self):
        return random.choice([
            None,
            {},
            [],
            "",
            0,
            -1,
            999999999999,
            ''.join(random.choices(string.ascii_letters +
                                   string.digits, k=10)),
            [random.randint(1000, 9999)],
            {"coffee": "text", "addons": "string"}
        ])

    def test_fuzz_create_order(self):
        url = reverse('create-order')

        for i in range(20):
            random_items = [self.generate_random_value()
                            for _ in range(random.randint(1, 3))]

            data = {
                "items": random_items
            }

            self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid.token')

            response = self.client.post(url, data, format='json')

            self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST,
                                                 status.HTTP_401_UNAUTHORIZED],
                          msg=f"Unexpected status code {response.status_code} "
                          "for input: {data}")
