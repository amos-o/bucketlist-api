"""Import statements."""
import unittest
from resources.resource_definitions import api, Allbucketlists, Login, Logout
from base import BaseTestCase
import json


class TestUserLogin(BaseTestCase):
    """Tests for cases related to logging in."""

    def test_unloggedin_user_cant_access_bucketlists(self):
        """Test that an unlogged in user can't access bucketlists resource."""
        response = self.client.get(api.url_for(Allbucketlists))

        self.assertEqual(response.status_code, 401)
        self.assertIn('Unauthorized Access', response.data)

if __name__ == '__main__':
    unittest.main()
