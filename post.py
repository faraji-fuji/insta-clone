from google.cloud import datastore
from google.cloud import storage
from google.auth.transport import requests
from pprint import pprint
import datetime
import google.oauth2.id_token
import local_constants


class Post():
    def __init__(self):
        # datastore
        self.datastore_client = datastore.Client()
        self.firebase_request_adapter = requests.Request()

        # storage
        self.storage_client = storage.Client(project=local_constants.PROJECT_NAME)
        self.bucket = self.storage_client.bucket(local_constants.PROJECT_STORAGE_BUCKET)

    def create_post(self, user_id, caption, image_url):
        '''
        Create a post entity.

        :param email: ID of ancestor entity.
        :param id: ID of post entity
        '''
        post_entity = datastore.Entity(key= self.datastore_client.key('User', user_id, 'Post'))
        post_entity.update({
            'likes': 0,
            'publisher': user_id,
            'comments': [],
            'caption': caption,
            'image_url': image_url,
            'date_created': datetime.datetime.now()
        })
        self.datastore_client.put(post_entity)

    def upload_file(self, file):
        '''
        Upload a file to google storage bucket

        :param file: The file to be uploaded.
        :returns: The public url of the file.
        '''
        blob = self.bucket.blob(file.filename)
        blob.upload_from_file(file)
        blob.make_public()

        return blob.public_url

    def get_posts(self, user_id):
        '''
        Get all the posts of the current user.
        '''
        ancestor_key = self.datastore_client.key('User', user_id)
        query = self.datastore_client.query(kind='Post', ancestor=ancestor_key)
        query.order = ['-date_created']
        posts = query.fetch()

        return posts

