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


class GetLecturesTest(ApiTestCase):
    def test_bad_request(self):
        resp = self.client.get(reverse('api_v1:lectures'), {})
        self.assert_resp_status(resp, 400, 'Must return bad request')

    def test_get_not_existing_lectures(self):
        resp = self.client.get(reverse('api_v1:lectures'), {'accounts': 'dgrdg,eqweq'})
        self.assert_api_success(resp, 'Must return success response')
        self.assertEqual(len(resp.json()) == 0, True, 'Must return empty list')

    def test_get_existing_lectures(self):
        account1 = Lecture.objects.create(
            account_name='test_account1',
            topic_id='42342_123'
        )
        account2 = Lecture.objects.create(
            account_name='test_account2',
            topic_id='42342_17734'
        )
        resp = self.client.get(reverse('api_v1:lectures'),
                                {'accounts': '%s,eqweq,%s' % (account1.account_name, account2.account_name)}
                               )
        self.assert_api_success(resp, 'Must return success response')
        self.assertEqual(len(resp.json()) > 0, True, 'Must return non empty list')
        self.assertEqual(
            len([data['account_name'] for data in resp.json()
                 if data['account_name'] in [account1.account_name, account2.account_name]]) == 2,
            True, 'Must find both existings accounts')
