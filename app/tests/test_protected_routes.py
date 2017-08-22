
import unittest
from app.views import app, is_testing

class ProtectedRoutesTestCase(unittest.TestCase):
    """This class represents the sign up test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        is_testing()
        self.app = app
        self.client = self.app.test_client

    def test_create_shopping_list(self):
        """Test API wont submit if user is not authorized (POST request)"""

        res = self.client().post('/shoppinglists/')
        self.assertEqual(res.status_code, 401)

    def test_retrieve_shopping_list(self):
        """Test API wont submit if user is not authorized (GET request)"""

        res = self.client().get('/shoppinglists/')
        self.assertEqual(res.status_code, 401)

    def test_retrieve_shopping_list_items(self):
        """Test API wont retirve resources if user is not authorized (GET request)"""

        res = self.client().get('/shoppinglists/1')
        self.assertEqual(res.status_code, 401)

    def test_update_shopping_list(self):
        """Test API wont submit if user is not authorized (PUT request)"""

        res = self.client().put('/shoppinglists/1', headers={'Content-Type': 'application/x-www-form-urlencoded'})
        self.assertEqual(res.status_code, 401)

    def test_delete_shopping_list(self):
        """Test API wont submit if user is not authorized (DELETE request)"""

        res = self.client().delete('/shoppinglists/1', headers={'Content-Type': 'application/x-www-form-urlencoded'})
        self.assertEqual(res.status_code, 401)




    def test_create_shopping_list_item(self):
        """Test API wont submit if user is not authorized (POST request)"""

        res = self.client().post('/shoppinglists/1/items')
        self.assertEqual(res.status_code, 401)

    def test_update_shopping_list_item(self):
        """Test API wont submit if user is not authorized (PUT request)"""

        res = self.client().put('/shoppinglists/1/items/1', headers={'Content-Type': 'application/x-www-form-urlencoded'})
        self.assertEqual(res.status_code, 401)

    def test_delete_shopping_list_item(self):
        """Test API wont submit if user is not authorized (DELETE request)"""

        res = self.client().delete('/shoppinglists/1/items/1', headers={'Content-Type': 'application/x-www-form-urlencoded'})
        self.assertEqual(res.status_code, 401)