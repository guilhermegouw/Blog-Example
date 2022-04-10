from urllib import response
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Post


class PostTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", email="testuser@email.com", password="secret"
        )
        self.post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            author=self.user,
            body="Body full of content",
        )
        self.published_post = Post.objects.create(
            title="Another Post",
            slug="another-post",
            author=self.user,
            body="Another body full of content",
            status="published",
        )

    def test_string_representation(self):
        self.assertEqual(str(self.post), "Test Post")

    def test_post_content(self):
        post = self.post
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.slug, "test-post")
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.body, "Body full of content")

    def test_published_manager(self):
        post = Post.published.filter(title__contains="Post")
        self.assertEqual(post.get(), self.published_post)


class PostListViewTests(TestCase):
    def test_post_list_view_status_code(self):
        response = self.client.get("/blog/")
        self.assertEqual(response.status_code, 200)


class PostDetailViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", email="testuser@email.com", password="secret"
        )
        self.post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            author=self.user,
            body="Body full of content",
        )
        self.published_post = Post.objects.create(
            title="Another Post",
            slug="another-post",
            author=self.user,
            body="Another body full of content",
            status="published",
        )

    def test_post_detail_view_status_code(self):
        published_post_url = self.published_post.get_absolute_url()
        response = self.client.get(published_post_url)
        self.assertEqual(response.status_code, 200)
