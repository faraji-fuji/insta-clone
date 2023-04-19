from google.cloud import datastore
from google.auth.transport import requests
from pprint import pprint
import datetime
import google.oauth2.id_token


class User():
    def __init__(self):
        self.datastore_client = datastore.Client()
        self.firebase_request_adapter = requests.Request()

    def create_user(self, user_id):
        '''
        Create user entity.

        :param user_id: The id of the user entity
        '''
        entity_key = self.datastore_client.key('User', user_id)
        entity = datastore.Entity(key=entity_key)
        entity.update({
            'setup': 0
        })
        self.datastore_client.put(entity)

    def setup_user(self):
        pass

    def get_user(self, user_id):
        '''
        Get a user entity from datastore.

        :param user_id: The id of the entity.
        '''
        user_key = self.datastore_client.key('User', user_id)
        user_entity = self.datastore_client.get(user_key)
        return user_entity

    def update_user_username(self, user_id, username):
        '''
        Update user entity.

        :param user_id: The id of the user entity.
        :param name: The name property of the entity
        '''
        entity_key = self.datastore_client.key('User', user_id)
        entity = datastore.Entity(key=entity_key)
        entity.update({
            'username': username
        })
        self.datastore_client.put(entity)

    def update_user_profile_name(self, user_id, profile_name):
        '''
        Update user entity.

        :param user_id: The id of the user entity.
        :param name: The name property of the entity
        '''
        entity_key = self.datastore_client.key('User', user_id)
        entity = datastore.Entity(key=entity_key)
        entity.update({
            'profile_name': profile_name
        })
        self.datastore_client.put(entity)

    def update_user_username(self, user_id, name):
        '''
        Update user entity.

        :param user_id: The id of the user entity.
        :param name: The name property of the entity
        '''
        entity_key = self.datastore_client.key('User', user_id)
        entity = datastore.Entity(key=entity_key)
        entity.update({
            'user_id': user_id
        })
        self.datastore_client.put(entity)
