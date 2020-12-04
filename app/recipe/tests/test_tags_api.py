from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer


TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase):
    """Test publicly available API tags"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        """Test that we reqiuire authenticated user to get tags"""
        response = self.client.get(TAGS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTest(TestCase):
    """Test tags with authorized user"""

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            email='test@email.com',
            password='test-pass'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test getting list of tags"""
        Tag.objects.create(user=self.user, name='Dessert')
        Tag.objects.create(user=self.user, name='Burger')

        response = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_tags_limited_to_self_user(self):
        """Test that the tags we return are for the authenticated user"""
        other_user = get_user_model().objects.create_user(
            email='other-user@email.com',
            password='test-pass'
        )

        Tag.objects.create(user=other_user, name='Nuts')
        tag = Tag.objects.create(user=self.user, name='Mexican')

        response = self.client.get(TAGS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], tag.name)
