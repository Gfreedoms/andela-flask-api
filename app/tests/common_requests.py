
import unittest
from base64 import b64encode

from flask import json
from app.views import app
from app.models import db


class CommonRequests(unittest.TestCase):

    def define_db_connections(self, app):
        POSTGRES = {
            'user': 'postgres',
            'pw': '',
            'db': 'testdb',
            'host': 'localhost',
            'port': '5432',
        }

        app.config["SQLALCHEMY_DATABASE_URI"] = \
            'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES


    def setUp(self):
        self.set_up_tests()

    def set_up_tests(self):
        """Define test variables and initialize app."""
        self.app = app
        self.define_db_connections(self.app)

        self.client = self.app.test_client

        self.sign_up_credentials = {
            'username': 'vince',
            "email": "vincenthokie@gmail.com",
            "password": "123",
            "password2": "123"}

        self.credentials = {"username": "a", "password": "a"}

        self.login_credentials = {'username': 'vince', "password": "123"}

        self.shopping_list = {'name': 'ListThing'}

        self.token = ""
        self.list_id = ""

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def set_up_authorized_route(self):
        with app.test_client() as client:
            res = self.login(client, self.login_credentials)

            token = json.loads(res.data)
            self.token = token["token"]

    # authentication methods
    def login(self, client,  login_credentials):
        return client.post('/auth/login', data=login_credentials)

    def sign_up(self, client, sign_up_credentials):
        return client.post('/auth/register', data=sign_up_credentials)

    def logout(self, client):
        return client.post('/auth/logout',
                           headers=self.get_auth_header())

    def get_auth_header(self):
        return {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic %s' % b64encode(
                bytes(self.token + ':x', "utf-8")).decode("ascii")
        }

    # crud on a shopping list
    def get_all_shopping_list(self, client, list_id=""):

        if list_id is not "":
            list_id = "?list_id="+list_id

        return client.get('/shoppinglists'+list_id,
                          headers=self.get_auth_header())

    def create_shopping_list(self, client,  shopping_list):
        return client.post('/shoppinglists', data=shopping_list,
                           headers=self.get_auth_header())

    def update_shopping_list(self, client,  shopping_list, list_id):
        headers=self.get_auth_header()
        headers["Content-Type"] = 'application/x-www-form-urlencoded'
        return client.put('/shoppinglists/'+str(list_id),
                          data=shopping_list, headers=headers)

    def delete_shopping_list(self, client, list_id):
        headers = self.get_auth_header()
        headers["Content-Type"] = 'application/x-www-form-urlencoded'
        return client.delete('/shoppinglists/'+str(list_id), headers=headers)

    # crud on a shopping list items
    def get_items_under_shopping_list(self, client, list_id):
        return client.get('/shoppinglists/'+str(list_id),
                          headers=self.get_auth_header())

    def create_shopping_list_item(self, client, shopping_list_item, list_id):
        return client.post('/shoppinglists/'+str(list_id)+'/items',
                           data=shopping_list_item,
                           headers=self.get_auth_header())

    def update_shopping_list_item(self, client, shopping_list_item, list_id,
                                  item_id):
        return client.put('/shoppinglists/'+str(list_id)+'/items/'+str(item_id),
                          data=shopping_list_item,
                          headers=self.get_auth_header())

    def delete_shopping_list_item(self, client, list_id, item_id):
        return client.delete('/shoppinglists/'+str(list_id)+'/items/'+
                             str(item_id), headers=self.get_auth_header())

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()