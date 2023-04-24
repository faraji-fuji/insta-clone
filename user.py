# from google.cloud import datastore
# from google.auth.transport import requests
# from pprint import pprint
# import datetime
# import google.oauth2.id_token


# class User():
#     def __init__(self):
#         self.datastore_client = datastore.Client()
#         self.firebase_request_adapter = requests.Request()

# def create_user(self, user_id):
#     '''
#     Create user entity.

#     :param user_id: The id of the user entity
#     '''
#     entity_key = self.datastore_client.key('User', user_id)
#     entity = datastore.Entity(key=entity_key)
#     entity.update({
#         'setup': 0
#     })
#     self.datastore_client.put(entity)

# def setup_user(self):
#     pass

# def get_user(self, user_id):
#     ''' Get a user entity from datastore.

#     :param user_id: The id of the entity.
#     '''
#     user_key = self.datastore_client.key('User', user_id)
#     user_entity = self.datastore_client.get(user_key)
#     return user_entity

# def update_user_username(self, user_id, username):
#     ''' Update user entity.

#     :param user_id: The id of the user entity.
#     :param name: The name property of the entity
#     '''
#     entity_key = self.datastore_client.key('User', user_id)
#     entity = datastore.Entity(key=entity_key)
#     entity.update({
#         'username': username
#     })
#     self.datastore_client.put(entity)

# def update_user_profile_name(self, user_id, profile_name):
#     ''' Update user entity.

#     :param user_id: The id of the user entity.
#     :param name: The name property of the entity
#     '''
#     entity_key = self.datastore_client.key('User', user_id)
#     entity = datastore.Entity(key=entity_key)
#     entity.update({
#         'profile_name': profile_name
#     })
#     self.datastore_client.put(entity)

# def update_user_username(self, user_id, name):
#     ''' Update user entity.

#     :param user_id: The id of the user entity.
#     :param name: The name property of the entity
#     '''
#     entity_key = self.datastore_client.key('User', user_id)
#     entity = datastore.Entity(key=entity_key)
#     entity.update({
#         'user_id': user_id
#     })
#     self.datastore_client.put(entity)

# def follow_user(self, user_id, follow_user_id):
#     ''' Follow a user.

#     :param user_id: The identifier of the current user.
#     :param follow_user_id: The identifier of the user to follow.
#     '''
# get entities involved, best alternative
# user_entity_key = self.datastore_client.key('User', user_id)
# follow_user_entity_key = self.datastore_client.key('User', follow_user_entity)
# entities = self.datastore_client.get_multi([user_entity_key, follow_user_entity_key])

# # get entities involved
# user_entity = self.get_user(user_id)
# follow_user_entity = self.get_user(follow_user_id)

# # add follow_user_id to the current user's following list
# following = user_entity['following']

# if follow_user_id not in following:
#     following.append(follow_user_id)
#     user_entity.update({
#         'following': following
#     })

#     # add user_id to followers list of the account being followed
#     followers = follow_user_entity['followers']
#     followers.append(user_id)
#     follow_user_entity.update({
#         'followers': followers
#     })

#     # commit the changes as a transaction
#     transaction = self.datastore_client.transaction()
#     with transaction:
#         transaction.put(user_entity)
#         transaction.put(follow_user_entity)

# def unfollow_user(self, user_id, unfollow_user_id):
#     ''' Unfollow a user.

#     :param user_id: The identifier ot the current user.
#     :param unfollow_user_id: The identifier of the user to unfollow.
#     '''
# user_entity = self.get_user(user_id)
# unfollow_user_entity = self.get_user(unfollow_user_id)

# # remove follow_user_id to the current user's following list
# following = user_entity['following']
# if unfollow_user_id in following:
#     following.remove(unfollow_user_id)
#     user_entity.update({
#         'following': following
#     })

#     # remove user_id to followers list of the account being followed
#     followers = unfollow_user_entity['followers']
#     followers.remove(user_id)
#     unfollow_user_entity.update({
#         'followers': followers
#     })

#     # commit the changes as a transaction
#     transaction = self.datastore_client.transaction()
#     with transaction:
#         transaction.put(user_entity)
#         transaction.put(unfollow_user_entity)
