from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Post


class PostListCreateTests(APITestCase):
    url = "/careers/"

    def _create_post(self, **kwargs):
        defaults = {"username": "alice", "title": "Hello", "content": "World"}
        defaults.update(kwargs)
        return Post.objects.create(**defaults)

    # ── GET /careers/ ──────────────────────────────────────────────
    def test_list_empty(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 0)
        self.assertEqual(res.data["results"], [])

    def test_list_ordered_by_most_recent_first(self):
        p1 = self._create_post(title="First")
        p2 = self._create_post(title="Second")
        res = self.client.get(self.url)
        ids = [item["id"] for item in res.data["results"]]
        self.assertEqual(ids, [p2.id, p1.id])

    def test_list_pagination_keys_present(self):
        res = self.client.get(self.url)
        for key in ("count", "next", "previous", "results"):
            self.assertIn(key, res.data)

    def test_list_page_size_param(self):
        for i in range(15):
            self._create_post(title=f"Post {i}")
        res = self.client.get(self.url + "?page_size=5")
        self.assertEqual(len(res.data["results"]), 5)
        self.assertEqual(res.data["count"], 15)

    # ── POST /careers/ ─────────────────────────────────────────────
    def test_create_post(self):
        payload = {"username": "bob", "title": "My Post", "content": "Some content"}
        res = self.client.post(self.url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)

    def test_create_response_shape(self):
        payload = {"username": "bob", "title": "My Post", "content": "Content"}
        res = self.client.post(self.url, payload, format="json")
        for field in ("id", "username", "created_datetime", "title", "content"):
            self.assertIn(field, res.data)

    def test_create_missing_field_returns_400(self):
        res = self.client.post(self.url, {"username": "bob"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class PostDetailTests(APITestCase):
    def setUp(self):
        self.post = Post.objects.create(
            username="carol", title="Original Title", content="Original Content"
        )
        self.url = f"/careers/{self.post.id}/"

    # ── PATCH /careers/{id}/ ───────────────────────────────────────
    def test_patch_title_and_content(self):
        payload = {"title": "Updated Title", "content": "Updated Content"}
        res = self.client.patch(self.url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Updated Title")
        self.assertEqual(self.post.content, "Updated Content")

    def test_patch_partial_only_title(self):
        res = self.client.patch(self.url, {"title": "New Title"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "New Title")
        self.assertEqual(self.post.content, "Original Content")

    def test_patch_cannot_change_username(self):
        res = self.client.patch(self.url, {"username": "hacker"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.username, "carol")  # unchanged

    def test_patch_cannot_change_id(self):
        original_id = self.post.id
        self.client.patch(self.url, {"id": 9999}, format="json")
        self.post.refresh_from_db()
        self.assertEqual(self.post.id, original_id)

    def test_patch_nonexistent_returns_404(self):
        res = self.client.patch("/careers/9999/", {"title": "X"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    # ── DELETE /careers/{id}/ ──────────────────────────────────────
    def test_delete_post(self):
        res = self.client.delete(self.url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_delete_nonexistent_returns_404(self):
        res = self.client.delete("/careers/9999/")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    # ── Method restrictions ────────────────────────────────────────
    def test_put_not_allowed(self):
        res = self.client.put(self.url, {"title": "X", "content": "Y"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
