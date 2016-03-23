"""Import statements."""
import json
import unittest

from resources.resource_definitions import api, Bucketlistitem,\
    Bucketitemsactions, Login, Logout, Allbucketlists

from base import BaseTestCase


class TestBucketlistItemActions(BaseTestCase):
    """
    Test for actions related to bucketlist items.

    Actions include creating a bucket list item, updating a bucket list
    item and deleting a bucketlist item.
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

    def test_user_can_create_bucketlist_item(self):
        """Test that a user can create bucketlist items."""
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

        # create a test Bucketlist item
        response1 = self.client.post(
                         api.url_for(Bucketlistitem, id=1),
                         data=json.dumps({"name": "Travel to Iceland."}),
                         content_type='application/json',
                         headers={'Authorization': token}
                         )

        # test item was created
        self.assertEqual(response1.status_code, 200)
        data = json.loads(response1.data)
        self.assertIn("Travel to Iceland.", data['items'][0]['name'])

    def test_user_can_update_a_bucketlist_item(self):
        """Test that a user can update bucketlist items"""
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

        # create a test Bucketlist item
        response1 = self.client.post(
                         api.url_for(Bucketlistitem, id=1),
                         data=json.dumps({"name": "Travel to Iceland."}),
                         content_type='application/json',
                         headers={'Authorization': token}
                         )

        # update the item
        response2 = self.client.put(
                         api.url_for(Bucketitemsactions, id=1, item_id=1),
                         data=json.dumps({"name": "Travel to Iceland updated."}),
                         content_type='application/json',
                         headers={'Authorization': token}
                         )

        # test item was updated
        self.assertEqual(response2.status_code, 200)
        data = json.loads(response2.data)
        self.assertIn("Travel to Iceland updated.", data['name'])

    def test_user_can_delete_a_bucketlist_item(self):
        """Test that a user can delete a bucketlist item."""
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

        # create a test Bucketlist item
        response1 = self.client.post(
                         api.url_for(Bucketlistitem, id=1),
                         data=json.dumps({"name": "Travel to Iceland."}),
                         content_type='application/json',
                         headers={'Authorization': token}
                         )

        # delete the item
        response2 = self.client.delete(
                         api.url_for(Bucketitemsactions, id=1, item_id=1),
                         content_type='application/json',
                         headers={'Authorization': token}
                         )

        # test item was deleted
        self.assertEqual(response2.status_code, 200)
        data = json.loads(response2.data)
        self.assertIn("Item 1 from bucketlist 1 deleted successfully.", data['message'])

    def test_for_error_conditions(self):
        """Test for error conditions."""
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

        # create a test Bucketlist item
        response1 = self.client.post(
                         api.url_for(Bucketlistitem, id=1),
                         data=json.dumps({"name": "Travel to Iceland."}),
                         content_type='application/json',
                         headers={'Authorization': token}
                         )

        # test someone can't update item in nonexistent bucketlist
        response2 = self.client.put(
                         api.url_for(Bucketitemsactions, id=10, item_id=1),
                         data=json.dumps({"name": "Travel to Iceland updated."}),
                         content_type='application/json',
                         headers={'Authorization': token}
                         )

        self.assertEqual(response2.status_code, 404)
        data = json.loads(response2.data)
        self.assertIn("Bucketlist item not found", data['Error'])

        # test someone can't delete nonexistent item
        response3 = self.client.delete(
                         api.url_for(Bucketitemsactions, id=1, item_id=2),
                         content_type='application/json',
                         headers={'Authorization': token}
                         )

        self.assertEqual(response3.status_code, 404)
        data = json.loads(response3.data)
        self.assertIn("Bucketlist has no item with id 2", data['Error'])
