from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTest(TestCase):

    def test_wait_for_db_ready(self):
        """Test the command to wait for db until it's ready"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as get_item:
            get_item.return_value = True
            call_command('wait_for_db')
            # Check if our db was called just once
            self.assertEqual(get_item.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db_(self, ts):
        """Test waiting for db command, we also mock the time sleep as we don't really want to wait it in tests"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as get_item:
            # Mock 5 operation errors and a success right after
            get_item.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(get_item.call_count, 6)