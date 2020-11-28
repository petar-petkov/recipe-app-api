from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    """This is just testing our own customizations such as the custom user"""

    def setUp(self):
        password = 'password123'
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin_user@email.com",
            password=password
        )
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email="user@email.com",
            password=password,
            name='User Name'
        )

    def test_users_listed(self):
        """Test that users are listed on the admin user page"""
        url = reverse('admin:core_user_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_user_edit_page(self):
        """Test if the admin edit page works"""

        # /admin/core/user/id
        url = reverse('admin:core_user_change', args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_create_new_user_page(self):
        """Test that our create user page works"""
        url = reverse('admin:core_user_add')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
