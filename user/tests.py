from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class UserCreationTests(APITestCase):
    def test_create_user(self):
        url = reverse("user:create")
        data = {"email": "test@example.com", "password": "password123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(
            get_user_model().objects.get().email, "test@example.com"
        )


class JWTTokenTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="password123"
        )
        self.url = reverse("user:token_obtain_pair")

    def test_token_obtain_pair(self):
        data = {"email": "test@example.com", "password": "password123"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)


class JWTTokenRefreshTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="password123"
        )
        self.refresh_token = str(RefreshToken.for_user(self.user))
        self.url = reverse("user:token_refresh")

    def test_token_refresh(self):
        data = {"refresh": self.refresh_token}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)


class JWTTokenVerifyTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="password123"
        )
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.url = reverse("user:token_verify")

    def test_token_verify(self):
        data = {"token": self.token}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ManageUserTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="password123"
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("user:manage")

    def test_get_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_update_user(self):
        data = {"email": "updated@example.com", "password": "newpassword123"}
        response = self.client.patch(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "updated@example.com")
        self.assertTrue(self.user.check_password("newpassword123"))
