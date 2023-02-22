from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

TOKEN_URL = reverse("user:token")


def create_user(email="user@example.com", password="test123!@#"):
    user = get_user_model().objects.create_user(email, password)
    return user


class PrivateTestUserApi(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_create_token_for_user(self):
        email = "user1@example.com"
        password = "test123!@#"

        user = create_user(email, password)
        payload = dict(email=email, password=password)

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
