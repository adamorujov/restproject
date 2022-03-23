from pickle import TRUE
from re import A
from xml.etree.ElementTree import TreeBuilder
from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from post.models import Post
from django.contrib.auth.models import User


class PostListCreateAPITestCase(APITestCase):
    url_list = reverse("post:list")
    url_create = reverse("post:create")
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username1 = "orucovadem"
        self.password1 = "Adem+224455"
        self.username2 = "ademorucov"
        self.password2 = "Adem+554422"
        self.user1 = User.objects.create_user(username=self.username1, password=self.password1, is_staff=True)
        self.user2 = User.objects.create_user(username=self.username2, password=self.password2)
        self.post = Post.objects.create(user=self.user1, title="Example title", content="Example content")

    def login_with_staff(self):
        data = {
            "username": self.username1,
            "password": self.password1
        }
        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in response.data)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+token)

    def login_with_not_staff(self):
        data = {
            "username": self.username2,
            "password": self.password2
        }
        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in response.data)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+token)

    def test_get_list_page(self):
        response = self.client.get(self.url_list)
        self.assertEqual(200, response.status_code)

    def test_get_create_page_with_guest(self):
        response = self.client.get(self.url_create)
        self.assertEqual(401, response.status_code)

    def test_get_create_page_with_not_staff(self):
        self.login_with_not_staff()
        response = self.client.get(self.url_create)
        self.assertEqual(403, response.status_code)

    def test_get_create_page_with_staff(self):
        self.login_with_staff()
        response = self.client.get(self.url_create)
        self.assertEqual(405, response.status_code)

    def test_create_with_valid_data(self):
        self.login_with_staff()
        data = {
            "title": "Test title",
            "content": "Test content",
            "user": self.user1.id
        }
        response = self.client.post(self.url_create, data)
        self.assertEqual(201, response.status_code)

    def test_create_with_invalid_data(self):
        self.login_with_staff()
        data = {
            "title": "",
            "content": "",
        }
        response = self.client.post(self.url_create, data)
        self.assertEqual(400, response.status_code)

class PostRetrieveUpdateDestroyAPITestCase(APITestCase):
    def setUp(self):
        self.username1 = "orucovadem"
        self.password1 = "Adem+224455"
        self.user1 = User.objects.create_user(username=self.username1, password=self.password1, is_staff=True)
        self.post1 = Post.objects.create(user=self.user1, title="Example Title", content="Example Content")

        self.username2 = "ademorucov"
        self.password2 = "Adem+554422"
        self.user2 = User.objects.create_user(username=self.username2, password=self.password2)
        self.post2 = Post.objects.create(user=self.user2, title="Example Title", content="Example Content")

        self.url_detail = reverse("post:detail", kwargs={"slug": self.post1.slug})
        self.url_update = reverse("post:update", kwargs={"slug": self.post1.slug})
        self.url_delete = reverse("post:delete", kwargs={"slug": self.post1.slug})
        self.url_login = reverse("token_obtain_pair")

    def login_with_staff(self):
        data = {
            "username": self.username1,
            "password": self.password1
        }
        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in response.data)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+token)

    def login_with_not_staff(self):
        data = {
            "username": self.username2,
            "password": self.password2
        }
        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in response.data)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+token)

    def test_get_detail_page(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(200, response.status_code)

    def test_get_update_page_with_not_authenticated(self):
        response = self.client.get(self.url_update)
        self.assertEqual(401, response.status_code)

    def test_get_update_page_with_not_owner(self):
        self.login_with_not_staff()
        response = self.client.get(self.url_update)
        self.assertEqual(403, response.status_code)

    def test_get_update_page_with_owner_or_staff(self):
        self.login_with_staff()
        response = self.client.get(self.url_update)
        self.assertEqual(200, response.status_code)

    def test_update_with_valid_data(self):
        self.login_with_staff()
        data = {
            "title": "Test title",
            "content": "Test content",
            "user": self.user1.id
        }
        response = self.client.put(self.url_update, data)
        self.assertEqual(200, response.status_code)

    def test_update_with_invalid_data(self):
        self.login_with_staff()
        data = {
            "title": "",
        }
        response = self.client.put(self.url_update, data)
        self.assertEqual(400, response.status_code)

    def test_delete_page_with_not_authenticated(self):
        response = self.client.get(self.url_delete)
        self.assertEqual(401, response.status_code)

    def test_delete_page_with_not_owner(self):
        self.login_with_not_staff()
        response = self.client.get(self.url_delete)
        self.assertEqual(405, response.status_code)

    def test_delete_with_owner_or_staff(self):
        self.login_with_staff()
        response = self.client.delete(self.url_delete)
        self.assertEqual(204, response.status_code)
