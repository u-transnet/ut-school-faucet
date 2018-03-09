import json
from django.test import override_settings
from django.urls import reverse

from faucet.models import Account
from faucet.tests.utils import ApiTestCase
from faucet.views import AccountView
from faucet.configs import test_tokens


@override_settings(BLOCKCHAIN_NOBROADCAST=True)
class CreateAccountTest(ApiTestCase):
    FAKE_IP = '192.168.0.15'
    DEFAULT_NETWORK = Account.NETWORK_VK

    VALID_TEST_ACCOUNT_NAME = 'test_account23'
    VALID_TEST_ACCOUNT_SECOND_NAME = 'test_account22'
    PRIMARY_ACCOUNT_NAME = 'test_account'
    EXISTS_ACCOUNT_NAME = 'u-tech-faucet'

    def create_request_data(self, fields_values=None, missing_fields=None):
        if fields_values is None:
            fields_values = {}
        if missing_fields is None:
            missing_fields = []

        request_data = {
            "name": self.PRIMARY_ACCOUNT_NAME,
            "owner_key": 'test1',
            "active_key": 'test2',
            "memo_key": 'test3',
            "access_token": 'sometoken',
            "social_network": self.DEFAULT_NETWORK
        }

        for field_name in missing_fields:
            del request_data[field_name]

        request_data.update(fields_values)

        return request_data

    def send_request(self, request_data, use_fake_ip=False):
        ip = self.FAKE_IP if use_fake_ip else '127.0.0.1'
        return self.client.post(reverse('api_v1:accounts'), data=request_data,
                                REMOTE_ADDR=ip)

    def test_networks_recognition(self):
        networks = [Account.NETWORK_VK, Account.NETWORK_GOOGLE, Account.NETWORK_FACEBOOK, 'abracadabra']
        resp_codes = [200, 200, 200, 400]

        for resp_code, network in zip(resp_codes, networks):
            resp = self.send_request(self.create_request_data({
                'social_network': network
            }), False)
            self.assert_resp_status(resp, resp_code, 'Network %s failed' % network)

    def test_account_data(self):
        resp = self.client.post(reverse('api_v1:accounts'), {})
        self.assertEqual(resp.status_code, 400, 'Registration must reject empty response')

        resp = self.client.post(reverse('api_v1:accounts'), {})
        self.assert_resp_status(resp, 400)

        missing_keys = ['owner_key', 'active_key', 'memo_key']
        for key_name in missing_keys:
            resp = self.send_request(self.create_request_data(missing_fields=[key_name]), use_fake_ip=False)
            self.assert_resp_status(resp, 400)

    def test_ip(self):
        resp = self.send_request(self.create_request_data())
        self.assert_error_code(resp, AccountView.ERROR_INVALID_IP)

        account = Account.objects.create(
            name='test',
            ip=self.FAKE_IP,
            authorized_network=self.DEFAULT_NETWORK,
            uid='test',
            first_name='test',
            last_name='test'
        )

        resp = self.send_request(self.create_request_data(), use_fake_ip=True)
        self.assert_api_error(resp, AccountView.ERROR_DUPLICATE_ACCOUNT)

        account.delete()

    def test_account_validation(self):

        # Validate cheap name
        resp = self.send_request(self.create_request_data(), use_fake_ip=True)
        self.assert_error_code(resp, AccountView.ERROR_INVALID_ACCOUNT_NAME)

        resp = self.send_request(self.create_request_data(
            fields_values={'name': self.EXISTS_ACCOUNT_NAME},
        ), use_fake_ip=True)
        self.assert_error_code(resp, AccountView.ERROR_DUPLICATE_ACCOUNT)

    def test_referrer(self):
        resp = self.send_request(self.create_request_data(
            fields_values={
                'name': self.VALID_TEST_ACCOUNT_NAME,
                'referrer': self.VALID_TEST_ACCOUNT_SECOND_NAME
            },
        ), use_fake_ip=True)
        self.assert_error_code(resp, AccountView.ERROR_UNKNOWN_REFERRER)

    def test_sn_data_fetching(self):

        networks = [Account.NETWORK_VK, Account.NETWORK_GOOGLE, Account.NETWORK_FACEBOOK]
        tokens = [test_tokens.VK_ACCESS_TOKEN, test_tokens.GOOGLE_ACCESS_TOKEN, test_tokens.FACEBOOK_ACCESS_TOKEN]

        for network, access_token in zip(networks, tokens):
            resp = self.send_request(self.create_request_data(
                fields_values={
                    'name': self.VALID_TEST_ACCOUNT_NAME,
                    'access_token': 'invalid_token',
                    'social_network': network
                },
            ), use_fake_ip=True)
            self.assert_error_code(resp, AccountView.ERROR_SN_FETCH_DATA_ERROR)

            resp = self.send_request(self.create_request_data(
                fields_values={
                    'name': self.VALID_TEST_ACCOUNT_NAME,
                    'referrer': None,
                    'registrar': None,
                    'access_token': access_token,
                    'social_network': network
                },
            ), use_fake_ip=True)
            self.assert_resp_status(resp, 200)

            resp_data = resp.json()
            if 'error' in resp_data:
                self.assert_not_error_code(resp, AccountView.ERROR_SN_FETCH_DATA_ERROR,
                                           "Can't fetch data from %s with provided access_token %s" % (
                                               network, access_token))

    def test_account_creation(self):
        resp = self.send_request(self.create_request_data(
            fields_values={
                'name': self.VALID_TEST_ACCOUNT_NAME,
                'referrer': None,
                'registrar': None,
                'access_token': test_tokens.VK_ACCESS_TOKEN,
                'social_network': Account.NETWORK_VK
            },
        ), use_fake_ip=True)
        self.assert_resp_status(resp, 200)
        self.assert_api_success(resp, "Can't create account")

    def test_account_duplicate(self):
        self.test_account_creation()
        resp = self.send_request(self.create_request_data(
            fields_values={
                'name': self.VALID_TEST_ACCOUNT_NAME,
                'referrer': None,
                'registrar': None,
                'access_token': test_tokens.VK_ACCESS_TOKEN,
                'social_network': Account.NETWORK_VK
            },
        ), use_fake_ip=True)
        self.assert_error_code(resp, AccountView.ERROR_DUPLICATE_ACCOUNT)


class GetAccountsTest(ApiTestCase):
    def test_bad_request(self):
        resp = self.client.get(reverse('api_v1:accounts'), {})
        self.assert_resp_status(resp, 400, 'Must return bad request')

    def test_get_not_existing_accounts(self):
        resp = self.client.get(reverse('api_v1:accounts'), {'accounts': 'dgrdg,eqweq'})
        self.assert_api_success(resp, 'Must return success response')
        self.assertEqual(len(resp.json()) == 0, True, 'Must return empty list')

    def test_get_existing_accounts(self):
        account1 = Account.objects.create(
            name='test_account1',
            ip='127.63.534.123',
            authorized_network=Account.NETWORK_VK,
            uid='test1',
            first_name='test1',
            last_name='test2',
            photo='test3'
        )
        account2 = Account.objects.create(
            name='test_account2',
            ip='127.63.564.123',
            authorized_network=Account.NETWORK_VK,
            uid='test2',
            first_name='test3',
            last_name='test4',
            photo='test5'
        )
        resp = self.client.get(reverse('api_v1:accounts'),
                                {'accounts': '%s,eqweq,%s' % (account1.name, account2.name)}
                               )
        self.assert_api_success(resp, 'Must return success response')
        self.assertEqual(len(resp.json()) > 0, True, 'Must return non empty list')
        self.assertEqual(
            len([data['name'] for data in resp.json()
                 if data['name'] in [account1.name, account2.name]]) == 2,
            True, 'Must find both existing accounts')
