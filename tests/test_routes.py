"""Import statements."""
import json
import unittest

from resources.resource_definitions import api, Allbucketlists, Login, Logout
from base import BaseTestCase


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

    def logout(self, token):
        logout_response = self.client.get(
                        api.url_for(Logout),
                        content_type='application/json',
                        headers={'Authorization': token}
                        )

        return logout_response

    def test_unloggedin_user_cant_access_bucketlists(self):
        """Test that an unlogged in user can't access bucketlists resource."""
        response = self.client.get(api.url_for(Allbucketlists))

        self.assertEqual(response.status_code, 401)
        self.assertIn('Unauthorized Access', response.data)

    def test_login(self):
        response = self.login()

        self.assertEqual(response.status_code, 200)

        token = json.loads(response.data)
        self.assertTrue(token)

    # def test_logged_in_user_can_create_bucketlists(self):
    #     response = self.login()
    #     token = json.loads(response.data)
    #
    #     create_response = self.client.post(
    #                                  api.url_for(Allbucketlists),
    #                                  data=json.dumps({"name": "Life goals"}),
    #                                  content_type='application/json',
    #                                  headers={'Authorization': token}
    #                                  )
    #
    #     response2 = json.loads(create_response)
    #     self.assertTrue(response2)
    #     # self.assertEqual(response2.status_code, 200)
    #     # self.assertIn({"Bucketlist created successfully.", response2)

    def test_logged_in_user_can_access_bucketlists(self):
        response = self.login()
        token = json.loads(response.data)

        self.assertTrue(token)

        bucketlists = self.client.get(api.url_for(Allbucketlists),
                                                content_type='application/json',
                                                headers={'Authorization': token})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(bucketlists)
        # self.assertIn("l", token)

    def test_logout_works(self):
        response = self.login()
        token = json.loads(response.data)

        self.assertTrue(token)

        logout_response = self.logout(token)

        self.assertIn("You have been logged out successfully.", logout_response.data)

if __name__ == '__main__':
    unittest.main()
