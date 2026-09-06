from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Category, Post


class BlogTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pass12345")
        self.category = Category.objects.create(name="Django")
        self.post = Post.objects.create(
            title="Hello World",
            author=self.user,
            category=self.category,
            content="First post.",
        )

    def test_post_list_status(self):
        response = self.client.get(reverse("post-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello World")

    def test_category_filter(self):
        response = self.client.get(reverse("post-list"), {"category": "django"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello World")

    def test_create_requires_login(self):
        response = self.client.get(reverse("post-create"))
        self.assertEqual(response.status_code, 302)
