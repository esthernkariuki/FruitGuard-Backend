from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAuthTests(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.profile_url = reverse("profile")
        self.user_data = {
            "first_name": "Elizabeth",
            "last_name": "Barongo",
            "email": "elizabethmoraab@gmail.com",
            "phone_number": "0712345678",
            "password": "mypassword",
            "user_type": "agrovet", 
        }

    def test_user_can_register(self):
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(phone_number=self.user_data["phone_number"]).exists())
        self.assertTrue(User.objects.filter(email=self.user_data["email"]).exists())

    def test_user_can_login_and_get_token(self):
        User.objects.create_user(
            phone_number=self.user_data["phone_number"],
            email=self.user_data["email"],
            password=self.user_data["password"],
            first_name="Elizabeth",
            last_name="Barongo",
            user_type="agrovet",
        )
        response = self.client.post(self.login_url, {
            "phone_number": self.user_data["phone_number"],
            "password": self.user_data["password"]
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_access_profile_requires_authentication(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_access_profile_with_token(self):
        self.client.post(self.register_url, self.user_data, format="json")
        login_response = self.client.post(self.login_url, {
            "phone_number": self.user_data["phone_number"],
            "password": self.user_data["password"]
        }, format="json")
        token = login_response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["phone_number"], self.user_data["phone_number"])
        self.assertEqual(response.data["email"], self.user_data["email"])
