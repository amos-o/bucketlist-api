"""Import statements."""
import json
import unittest

from resources.resource_definitions import api, Allbucketlists, Login, \
    Logout, Onebucketlist, Home

from base import BaseTestCase


class TestBucketlistActions(BaseTestCase):
    """Tests for actions related to Bucketlists.

    Actions include accessing a bucketlist while not logged in,
    logging in, accessing all bucketlists, accessing a bucketlist by id,
    updating a bucketlist, deleting a bucketlist.
    """
    def login(self):
        """
        Method to log a test user in.

        Returns:
            The response of the login action
        """
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
        """
        Method to logout a test user.

        Returns:
            The response of the logout action
        """
        logout_response = self.client.get(
                        api.url_for(Logout),
                        content_type='application/json',
                        headers={'Authorization': token}
                        )

        return logout_response

    def test_accessing_home_returns_welcome_message(self):
        """Test that accessing home page returns a welcome message."""
        response = self.client.get(api.url_for(Home))

        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome to the bucketlist API.', response.data)

    def test_unlogged_in_user_cant_access_bucketlists(self):
        """Test that an unlogged in user can't access bucketlists resource."""
        response = self.client.get(api.url_for(Allbucketlists))

        self.assertEqual(response.status_code, 401)
        self.assertIn('Unauthorized Access', response.data)

    def test_login(self):
        """Test that logging in returns a token."""
        response = self.login()

        self.assertEqual(response.status_code, 200)

        reply = json.loads(response.data)
        token = reply['token']

        self.assertTrue(token)

    def test_authorized_user_can_create_bucketlists(self):
        """Test that a logged in user can create a bucketlist."""
        response = self.login()
        message = json.loads(response.data)
        token = message['token']

        response2 = self.client.post(
                                     api.url_for(Allbucketlists),
                                     data=json.dumps({"name": "Places I want to see"}),
                                     content_type='application/json',
                                     headers={'Authorization': token}
                                     )
        self.assertIn('Bucketlist created successfully.', response2.data)
        self.assertEqual(response2.status_code, 200)

    def test_authorized_user_can_access_all_bucketlists(self):
        """Test that a logged in user can see all his bucketlists."""
        response = self.login()
        message = json.loads(response.data)
        token = message['token']

        self.assertTrue(token)

        # create a test Bucketlist
        self.client.post(
                         api.url_for(Allbucketlists),
                         data=json.dumps({"name": "Life goals"}),
                         content_type='application/json',
                         headers={'Authorization': token}
                         )

        # get all the bucketlists
        bucketlists = self.client.get(api.url_for(Allbucketlists),
                                                content_type='application/json',
                                                headers={'Authorization': token})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(bucketlists)
        self.assertIn("Life goals", bucketlists.data)

    def test_authorized_user_can_access_bucketlist_by_id(self):
        """Test that a user can get one bucketlist by its id."""
        response = self.login()
        message = json.loads(response.data)
        token = message['token']

        self.assertTrue(token)

        # create a test Bucketlist
        self.client.post(
                         api.url_for(Allbucketlists),
                         data=json.dumps({"name": "Life goals"}),
                         content_type='application/json',
                         headers={'Authorization': token}
                         )

        # get the bucketlist by its id
        bucketlist = self.client.get(api.url_for(Onebucketlist, id=1),
                                                content_type='application/json',
                                                headers={'Authorization': token})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(bucketlist)
        self.assertIn("Life goals", bucketlist.data)

    def test_authorized_user_can_search_bucketlists(self):
        pass

    def test_authorized_user_can_edit_a_bucketlist(self):
        """Test that updating a bucketlist works as expected."""
        # login and get the token
        response = self.login()
        message = json.loads(response.data)
        token = message['token']

        # create a test Bucketlist
        self.client.post(
                         api.url_for(Allbucketlists),
                         data=json.dumps({"name": "Life goals"}),
                         content_type='application/json',
                         headers={'Authorization': token}
                         )

        # check the bucketlist is there
        bucketlists = self.client.get(api.url_for(Onebucketlist, id=1),
                                                content_type='application/json',
                                                headers={'Authorization': token})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(bucketlists)
        self.assertIn("Life goals", bucketlists.data)

        # update the bucketlist
        updated_bucketlist = self.client.put(
                         api.url_for(Onebucketlist, id=1),
                         data=json.dumps({"name": "Life goals forever"}),
                         content_type='application/json',
                         headers={'Authorization': token}
                         )

        # check bucketlist is actually updated
        self.assertTrue(updated_bucketlist)
        self.assertEqual(updated_bucketlist.status_code, 200)
        self.assertIn("Life goals forever", updated_bucketlist.data)

    def test_authorized_user_can_delete_a_bucketlist(self):
        """Test that a user can delete a bucketlist."""
        # login and get the token
        response = self.login()
        message = json.loads(response.data)
        token = message['token']

        # create a test Bucketlist
        self.client.post(
                         api.url_for(Allbucketlists),
                         data=json.dumps({"name": "Life goals"}),
                         content_type='application/json',
                         headers={'Authorization': token}
                         )

        # delete the bucketlist
        response = self.client.delete(
                         api.url_for(Onebucketlist, id=1),
                         content_type='application/json',
                         headers={'Authorization': token}
                         )

        self.assertIn("Bucketlist 1 deleted successfully.", response.data)

    def test_logout_works(self):
        """Test that a logout request returns correct response."""
        response = self.login()
        message = json.loads(response.data)
        token = message['token']

        self.assertTrue(token)

        logout_response = self.logout(token)

        self.assertIn("You have been logged out successfully.", logout_response.data)

if __name__ == '__main__':
    unittest.main()
