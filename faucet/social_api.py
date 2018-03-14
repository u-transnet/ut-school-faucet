import re

import facebook
import vk
from google.oauth2.credentials import Credentials
from googleapiclient import discovery


class VKApi(object):
    def __init__(self, token):
        session = vk.Session(access_token=token)
        self.api = vk.API(session, version='5.73')

    def __get_group_id_from_topic_url(self, url):
        result = re.compile('topic\-(\d+)\_\d+').search(url)
        return result.group(1)

    def get_user_info(self):
        user_data = self.api.users.get(fields=['photo_200', ])
        if not user_data:
            return None
        user_data = user_data[0]
        return {
            'uid': user_data['uid'],
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
            'photo': user_data['photo_200']
        }

    def check_is_topic_admin(self, topic_url):
        group_id = self.__get_group_id_from_topic_url(topic_url)
        groups = self.api.groups.getById(group_id=group_id, fields=['is_admin'])
        is_admin = False
        if groups:
            is_admin = int(groups[0]['is_admin']) == 1

        return is_admin


class GoogleApi(object):
    def __init__(self, token):
        credentials = Credentials(token=token)
        self.api = discovery.build("plus", "v1", credentials=credentials)

    def get_user_info(self):
        user_data = self.api.people().get(userId='me').execute()
        return {
            'uid': user_data.get('id'),
            'first_name': user_data['name'].get('givenName'),
            'last_name': user_data['name'].get('familyName'),
            'photo': user_data.get('image').get('url')
        }


class FacebookApi(object):
    def __init__(self, token):
        self.api = facebook.GraphAPI(access_token=token, version="2.1")

    def get_user_info(self):
        user_data = self.api.get_object('me', fields='id,first_name,last_name,cover')
        return {
            'uid': user_data.get('id'),
            'first_name': user_data.get('first_name'),
            'last_name': user_data.get('last_name'),
            'photo': user_data['cover']['source'] if 'cover' in user_data else ''
        }