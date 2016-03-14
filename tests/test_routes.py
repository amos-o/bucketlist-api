"""Import statements."""
# from models.bucketlist_model import app, BucketList, db
import unittest
from resources.resource_definitions import api, Allbucketlists
from base import BaseTestCase


class TestUserLogin(BaseTestCase):
    """Tests for cases related to logging in."""

    def login(self, username, password):
        """Call this to simulate a login with the test user."""
        return self.app.post('/auth/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        """Call this to simulate a logout with the test user."""
        return self.app.get('/auth/logout', follow_redirects=True)

    def test_unloggedin_user_cant_access_bucketlists(self):
        """Test that an unlogged in user can't access bucketlists resource."""
        response = self.client.get(api.url_for(Allbucketlists))

        self.assertEqual(response.status_code, 401)
        self.assertIn('Unauthorized Access', response.data)

if __name__ == '__main__':
    unittest.main()
