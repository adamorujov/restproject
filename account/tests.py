from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
import json


class UserRegistrationTestCase(APITestCase):
    url = reverse("account:create-user")
    url_login = reverse("token_obtain_pair")

    def test_user_registration(self):
        data = {
            "username": "orucovadem",
            "password": "Adem+224455",
        }

        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    def test_user_invalid_password(self):
        data = {
            "username": "orucovadem",
            "password": "1",
        }

        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)

    def test_unique_name(self):
        self.test_user_registration()

        data = {
            "username": "orucovadem",
            "password": "Adem22445566",
        }

        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)

    def test_user_authenticated_registration(self):
        self.test_user_registration()
        self.client.login(username="orucovadem", password="Adem+224455")
        response = self.client.get(self.url)
        self.assertEqual(403, response.status_code)

    def test_user_authenticated_token_registration(self):
        self.test_user_registration()
        
        data = {
            "username": "orucovadem",
            "password": "Adem+224455",
        }

        response_1 = self.client.post(self.url_login, data)
        self.assertEqual(200, response_1.status_code)

        access_token = response_1.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Beares'+access_token)
        response_2 = self.client.get(self.url)
        self.assertEqual(405, response_2.status_code)

class UserLoginTestCase(APITestCase):
    url_login = reverse('token_obtain_pair')

    def setUp(self):
        self.username = "orucovadem"
        self.password = "Adem+224455"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_user_token(self):
        response = self.client.post(
            self.url_login,
            {
                "username": "orucovadem",
                "password": "Adem+224455",
            }
        )
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))

    def test_user_invalid_data(self):
        response = self.client.post(
            self.url_login,
            {
                "username": "jmskjdknd",
                "password": "Adem+224455"
            }
        )
        self.assertEqual(401, response.status_code)

    def test_user_empty_data(self):
        response = self.client.post(
            self.url_login,
            {
                "username": "",
                "password": "",
            }
        )
        self.assertEqual(400, response.status_code)

class UserPasswordChangeTestCase(APITestCase):
    url = reverse("account:change-password")
    url_login = reverse('token_obtain_pair')

    def setUp(self):
        self.username = "orucovadem"
        self.password = "Adem+224455"
        self.user = User.objects.create_user(
            username = self.username,
            password = self.password,
        )

    def login_with_token(self):
        data = {
            "username": "orucovadem",
            "password": "Adem+224455",
        }
        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+token)

    def test_is_authenticated_user(self):
        response = self.client.get(self.url_login)
        self.assertEqual(405, response.status_code)

    def test_with_valid_data(self):
        self.login_with_token()
        data = {
            "old_password": "Adem+224455",
            "new_password": "Bingo+564930"
        }
        response = self.client.put(self.url, data)
        self.assertEqual(204, response.status_code)

    def test_with_wrong_data(self):
        self.login_with_token()
        data = {
            "old_password": "Adem++222235",
            "new_password": "Adem++233333"
        }
        response = self.client.put(self.url, data)
        self.assertEqual(400, response.status_code)

    def test_with_empty_data(self):
        self.login_with_token()
        data = {
            "old_password": "Adem+224455",
            "new_password": "",
        }
        response = self.client.put(self.url, data)
        self.assertEqual(400, response.status_code)

class UserUpdateTestCase(APITestCase):
    url = reverse("account:me")
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "orucovadem"
        self.password = "Adem+224455"
        self.user = User.objects.create_user(
            username = self.username,
            password = self.password,
        )

    def login_with_token(self):
        data = {
            "username": "orucovadem",
            "password": "Adem+224455"
        }
        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+token)

    def test_user_is_authenticated(self):
        response = self.client.get(self.url_login)
        self.assertEqual(405, response.status_code)

    def test_with_valid_data(self):
        self.login_with_token()
        data = {
            "username": "orucovadem",
            "password": "Adem+224455",
            "profile": {
                "note": "This is note.",
                "twitter": "https://help.twitter.com/en/forms/account-access/regain-access"
            }
        }

        response = self.client.put(self.url, data, format='json')
        self.assertEqual(200, response.status_code)

    def test_with_wrong_data(self):
        self.login_with_token()
        User.objects.create_user(
            username = "vasifkerimov",
            password = "f+22445566",
        )
        data = {
            "username": "vasifkerimov",
            "password": "Adem+++2244",
            "profile": {
                "note": "This is note.",
                "twitter": "https://help.twitter.com/en/forms/account-access/regain-access"
            }
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(400, response.status_code)

    def test_with_empty_data(self):
        self.login_with_token()
        data = {
            "username": "",
            "password": "",
            "profile": {
                "note": "This is note.",
                "twitter": "https://help.twitter.com/en/forms/account-access/regain-access"
            }
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(400, response.status_code)
