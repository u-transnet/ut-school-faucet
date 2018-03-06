import re

import vk


class VKApi(object):
    def __init__(self, token):
        session = vk.Session(access_token=token)
        self.api = vk.API(session)

    def __get_group_id_from_topic_url(self, url):
        result = re.compile('topic\-(\d+)\_\d+').search(url)
        return result.group(1)

    def check_is_topic_admin(self, topic_url):
        group_id = self.__get_group_id_from_topic_url(topic_url)
        groups = self.api.groups.getById(group_id=group_id, fields=['is_admin'])
        is_admin = False
        if groups:
            is_admin = int(groups[0]['is_admin']) == 1

        return is_admin
