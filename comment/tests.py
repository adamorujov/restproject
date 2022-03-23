from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from comment.models import Comment
from post.models import Post


class CommentListAPITestCase(APITestCase):
    url = reverse("comment:list")

    def test_get_list_page(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

class CommentCreateAPITestCase(APITestCase):
    url = reverse("comment:create")
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "orucovadem"
        self.password = "Adem+224455"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.post = Post.objects.create(user=self.user, title="Title", content="Content")
        self.comment = Comment.objects.create(user=self.user, post=self.post,  content="Content")

    def login_with_token(self):
        data = {
            "username": self.username,
            "password": self.password
        }
        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in response.data)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+token)

    def test_with_authenticated_user(self):
        self.login_with_token()
        response = self.client.get(self.url)
        self.assertEqual(405, response.status_code)

    def test_with_not_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)

    def test_with_valid_data(self):
        self.login_with_token()
        data = {
            "post": self.post.id,
            "parent": self.comment.id,
            "content": "Comment"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    def test_with_invalid_data(self):
        self.login_with_token()
        data = {
            "post": self.post.id,
            "parent": self.comment.id,
            "content": ""
        }
        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)

class CommentUpdateDestroyAPITestCase(APITestCase):
    def setUp(self):
        self.username = "orucovadem"
        self.password = "Adem+224455"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.post = Post.objects.create(user=self.user, title="Example title", content="Example content")
        self.comment = Comment.objects.create(user=self.user, post=self.post, content="Example comment")
        self.url = reverse("comment:update", kwargs={"pk": self.comment.id})
        self.url_login = reverse("token_obtain_pair")

    def login_with_token(self):
        data = {
            "username": self.username,
            "password": self.password
        }
        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in response.data)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+token)

    def test_with_not_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)

    def test_with_not_owner(self):
        self.user1 = User.objects.create_user(
            username="exampleuser",
            password="Test+224455"
        )
        data = {
            "username": "exampleuser",
            "password": "Test+224455"
        }
        response1 = self.client.post(self.url_login, data)
        self.assertEqual(200, response1.status_code)
        self.assertTrue("access" in response1.data)
        token = response1.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+token)

        response2 = self.client.get(self.url)
        self.assertEqual(403, response2.status_code)

    def test_with_owner(self):
        self.login_with_token()
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_with_valid_data(self):
        self.login_with_token()
        data = {
            "content": "Updated content",
        }
        response = self.client.put(self.url, data)
        self.assertEqual(200, response.status_code)

    def test_with_invalid_data(self):
        self.login_with_token()
        data = {
            "content": "",
        }
        response = self.client.put(self.url, data)
        self.assertEqual(400, response.status_code)

    def test_delete_comment(self):
        self.login_with_token()
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)