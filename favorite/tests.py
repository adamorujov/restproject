from dataclasses import dataclass
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from favorite.models import Favorite
from post.models import Post
import json


class FavoriteListTestCase(APITestCase):
    url = reverse("favorite:list")
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "orucovadem"
        self.password = "Adem+224455"
        User.objects.create_user(username=self.username, password=self.password)

    def login_with_token(self):
        data = {
            "username": self.username,
            "password": self.password,
        }
        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+token)

    def test_is_authenticated(self):
        self.login_with_token()
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_is_not_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)

class FavoriteCreateTestCase(APITestCase):
    url = reverse("favorite:create")
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "orucovadem"
        self.password = "Adem+224455"
        self.user = User.objects.create_user(username=self.username, password=self.password)

        self.post = Post.objects.create(user=self.user, title="Test example", content="Test example content")

    def login_with_token(self):
        data = {
            "username": self.username,
            "password": self.password,
        }
        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+token)

    def test_with_not_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)

    def test_with_authenticated(self):
        self.login_with_token()
        response = self.client.get(self.url)
        self.assertEqual(405, response.status_code)

    def test_create_with_valid_data(self):
        self.login_with_token()
        data = {
            "user": self.user.id,
            "post": self.post.id,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    def test_create_with_invalid_data(self):
        self.login_with_token()
        Favorite.objects.create(user=self.user, post=self.post)
        data = {
            "user": self.user.id,
            "post": self.post.id,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)

class FavoriteRetrieveUpdateDestroyTestCase(APITestCase):
    def setUp(self):
        self.username = "orucovadem"
        self.password = "Adem+224455"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.post = Post.objects.create(user=self.user, title="Test example", content="Test example content")
        self.favorite = Favorite.objects.create(user=self.user, post=self.post)
        self.url = reverse("favorite:retrieve-update-destroy", kwargs={"pk":self.favorite.id})
        self.url_login = reverse("token_obtain_pair")

    def login_with_token(self):
        data = {
            "username": self.username,
            "password": self.password
        }
        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+token)

    def test_with_not_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)

    def test_not_found(self):
        url_ = reverse("favorite:retrieve-update-destroy", kwargs={"pk":100})
        self.login_with_token()
        response = self.client.get(url_)
        self.assertEqual(404, response.status_code)

    def test_found(self):
        self.login_with_token()
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_destroy_not_found(self):
        url_ = reverse("favorite:retrieve-update-destroy", kwargs={"pk":100})
        self.login_with_token()
        response = self.client.delete(url_)
        self.assertEqual(404, response.status_code)

    def test_destroy(self):
        self.login_with_token()
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)
