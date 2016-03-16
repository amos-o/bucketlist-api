"""Import statements."""
import unittest
from resources.resource_definitions import api, Allbucketlists, Login, Logout
from base import BaseTestCase
import json


class TestUserLogin(BaseTestCase):
    """Tests for cases related to logging in."""
    def login(self):
        username = "amos"
        password = "12345"

        response = self.client.post(
                                    api.url_for(Login),
                                    data=json.dumps(
                                            {'username': username,
                                             'password': password
                                             }),
                                    content_type='application/json'
                                    )

        return response

    def test_unloggedin_user_cant_access_bucketlists(self):
        """Test that an unlogged in user can't access bucketlists resource."""
        response = self.client.get(api.url_for(Allbucketlists))

        self.assertEqual(response.status_code, 401)
        self.assertIn('Unauthorized Access', response.data)

    def test_login(self):
        response = self.login()

        self.assertEqual(response.status_code, 200)

        token = response.data
        self.assertTrue(token)

if __name__ == '__main__':
    unittest.main()
