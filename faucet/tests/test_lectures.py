from django.test import override_settings, TestCase
from django.urls import reverse

from faucet.configs import test_tokens
from faucet.models import Lecture, Account
from faucet.tests.utils import ApiTestCase
from faucet.views import LectureView


@override_settings(BLOCKCHAIN_NOBROADCAST=True)
class AddLectureTest(ApiTestCase):
    TEST_ACCOUNT = 'superpchelka23'
    TEST_ACCOUNT_INVALID = 'test_account31155'
    TOPIC_ID = '118718762_37342273'
    TOPIC_URL_VALID = 'https://vk.com/topic-%s' % TOPIC_ID
    TOPIC_URL_VALID_NOT_MINE = 'https://vk.com/topic-78553823_36635379'
    TOPIC_URL_INVALID = 'https://vk.com/topic-95883213_da318daw1'

    def test_fields_validation(self):
        data = {
            'account_name': self.TEST_ACCOUNT,
            'topic_url': self.TOPIC_URL_VALID,
            'access_token': test_tokens.VK_ACCESS_TOKEN
        }

        for key in data.keys():
            request_data = dict(data)
            del request_data[key]
            resp = self.client.post(reverse('api_v1:lectures'), request_data)
            self.assert_resp_status(resp, 400, "Must return bad request on missing fields")

        request_data = dict(data)
        request_data['topic_url'] = self.TOPIC_URL_INVALID
        resp = self.client.post(reverse('api_v1:lectures'), request_data)
        self.assert_resp_status(resp, 400, "Must return bad request on invalid topic_url")

    def test_fetching_data_from_social_network(self):
        request_data = {
            'account_name': self.TEST_ACCOUNT,
            'topic_url': self.TOPIC_URL_VALID,
            'access_token': 'fake_token'
        }
        resp = self.client.post(reverse('api_v1:lectures'), request_data)
        self.assert_api_error(resp, LectureView.ERROR_SN_FETCHING,
                              'Must return error about fetching data from social network')

    def test_admin_rights(self):
        request_data = {
            'account_name': self.TEST_ACCOUNT,
            'topic_url': self.TOPIC_URL_VALID_NOT_MINE,
            'access_token': test_tokens.VK_ACCESS_TOKEN
        }
        resp = self.client.post(reverse('api_v1:lectures'), request_data)
        self.assert_api_error(resp, LectureView.ERROR_SN_HAS_NO_PERMISSION)

        request_data['topic_url'] = self.TOPIC_URL_VALID
        resp = self.client.post(reverse('api_v1:lectures'), request_data)
        self.assert_api_success(resp)

    def test_account_does_not_exists(self):
        request_data = {
            'account_name': self.TEST_ACCOUNT_INVALID,
            'topic_url': self.TOPIC_URL_VALID,
            'access_token': test_tokens.VK_ACCESS_TOKEN
        }
        resp = self.client.post(reverse('api_v1:lectures'), request_data)
        self.assert_api_error(resp, LectureView.ERROR_ACCOUNT_DOES_NOT_EXISTS)


    def test_duplicate_error(self):

        Lecture.objects.create(
            account_name=self.TEST_ACCOUNT,
            topic_id=self.TOPIC_ID
        )

        request_data = {
            'account_name': self.TEST_ACCOUNT,
            'topic_url': self.TOPIC_URL_VALID,
            'access_token': test_tokens.VK_ACCESS_TOKEN
        }
        resp = self.client.post(reverse('api_v1:lectures'), request_data)
        self.assert_api_error(resp, LectureView.ERROR_DUPLICATE_LECTURE)


    def test_success_creation(self):
        request_data = {
            'account_name': self.TEST_ACCOUNT,
            'topic_url': self.TOPIC_URL_VALID,
            'access_token': test_tokens.VK_ACCESS_TOKEN
        }
        resp = self.client.post(reverse('api_v1:lectures'), request_data)
        self.assert_api_success(resp, 'Must create successfully create account')
