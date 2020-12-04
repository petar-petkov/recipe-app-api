from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Tag


def sample_user(email='test@email.com', password='test-pass'):
    """Create sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = "email@test.com"
        password = 'TestPass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_normalized_email(self):
        """Test if the email of a new user is normalized"""
        email = 'test@EMAIL.com'
        user = get_user_model().objects.create_user(email, 'test123123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email should raise an error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=None, password='123')

    def test_create_super_user(self):
        """Test if creating a new superuser works"""
        user = get_user_model().objects.create_superuser(
            email='test@email.com',
            password='test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test if our tags are strings"""
        tag = Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)
