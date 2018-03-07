import json
from django.test import TestCase, override_settings
from django.urls import reverse

from faucet.models import Account
from faucet.views import RegisterView
from faucet.configs import test_tokens


@override_settings(BLOCKCHAIN_NOBROADCAST=True)
class RegistrationTest(TestCase):
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

        account_obj = {
            "name": self.PRIMARY_ACCOUNT_NAME,
            "owner_key": 'test1',
            "active_key": 'test2',
            "memo_key": 'test3',
            "access_token": 'sometoken'
        }

        for field_name in missing_fields:
            del account_obj[field_name]

        account_obj.update(fields_values)

        return {
            'account': account_obj
        }

    def send_request(self, account_data, network=None, use_fake_ip=False):
        ip = self.FAKE_IP if use_fake_ip else '127.0.0.1'
        network = self.DEFAULT_NETWORK if network is None else network
        return self.client.post(reverse('register', args=[network]), json.dumps(account_data),
                                REMOTE_ADDR=ip, content_type='application/json')

    def assert_resp_status(self, resp, status, msg=None):
        if msg is None:
            msg = 'Must return status %s' % status
        self.assertEqual(resp.status_code, status, msg)

    def assert_error_code(self, resp, expected_code, msg=None):
        if msg is None:
            msg = 'Must correctly return error code'
        self.assertEqual(resp.json()['error']['code'], expected_code, msg)

    def assert_not_error_code(self, resp, expected_code, msg=None):
        if msg is None:
            msg = 'Must correctly return error code'
        self.assertNotEqual(resp.json()['error']['code'], expected_code, msg)

    def assert_api_error(self, resp, expected_code, msg=None):
        self.assert_resp_status(resp, 200)
        self.assert_error_code(resp, expected_code, msg)

    def test_networks_recognition(self):
        networks = [Account.NETWORK_VK, Account.NETWORK_GOOGLE, Account.NETWORK_FACEBOOK, 'abracadabra']
        resp_codes = [200, 200, 200, 400]

        for resp_code, network in zip(resp_codes, networks):
            resp = self.send_request(self.create_request_data(), network, False)
            self.assert_resp_status(resp, resp_code, 'Network %s failed' % network)

    def test_account_data(self):
        resp = self.client.post(reverse('register', args=[self.DEFAULT_NETWORK]), '', content_type='application/json')
        self.assertEqual(resp.status_code, 400, 'Registration must reject empty response')

        resp = self.client.post(reverse('register', args=[self.DEFAULT_NETWORK]), {}, content_type='application/json')
        self.assert_api_error(resp, RegisterView.ERROR_INVALID_ACCOUNT_DATA)

        missing_keys = ['owner_key', 'active_key', 'memo_key']
        for key_name in missing_keys:
            resp = self.send_request(self.create_request_data(missing_fields=[key_name]), use_fake_ip=False)
            self.assert_api_error(resp, RegisterView.ERROR_MISSING_PUBLIC_KEY)

    def test_ip(self):
        resp = self.send_request(self.create_request_data())
        self.assert_error_code(resp, RegisterView.ERROR_INVALID_IP)

        account = Account.objects.create(
            name='test',
            ip=self.FAKE_IP,
            authorized_network=self.DEFAULT_NETWORK,
            uid='test',
            first_name='test',
            last_name='test'
        )

        resp = self.send_request(self.create_request_data(), use_fake_ip=True)
        self.assert_api_error(resp, RegisterView.ERROR_DUPLICATE_ACCOUNT)

        account.delete()

    def test_account_validation(self):

        # Validate cheap name
        resp = self.send_request(self.create_request_data(), use_fake_ip=True)
        self.assert_error_code(resp, RegisterView.ERROR_INVALID_ACCOUNT_NAME)

        resp = self.send_request(self.create_request_data(
            fields_values={'name': self.VALID_TEST_ACCOUNT_NAME},
            missing_fields=['access_token']
        ), use_fake_ip=True)
        self.assert_error_code(resp, RegisterView.ERROR_MISSING_ACCOUNT_TOKEN)

        resp = self.send_request(self.create_request_data(
            fields_values={'name': self.EXISTS_ACCOUNT_NAME},
        ), use_fake_ip=True)
        self.assert_error_code(resp, RegisterView.ERROR_DUPLICATE_ACCOUNT)

    def test_registrar(self):
        resp = self.send_request(self.create_request_data(
            fields_values={
                'name': self.VALID_TEST_ACCOUNT_NAME,
                'registrar': self.VALID_TEST_ACCOUNT_SECOND_NAME
            },
        ), use_fake_ip=True)
        self.assert_error_code(resp, RegisterView.ERROR_UNKNOWN_REGISTRAR)

    def test_referrer(self):
        resp = self.send_request(self.create_request_data(
            fields_values={
                'name': self.VALID_TEST_ACCOUNT_NAME,
                'referrer': self.VALID_TEST_ACCOUNT_SECOND_NAME
            },
        ), use_fake_ip=True)
        self.assert_error_code(resp, RegisterView.ERROR_UNKNOWN_REFERRER)

    def test_sn_data_fetching(self):

        networks = [Account.NETWORK_VK, Account.NETWORK_GOOGLE, Account.NETWORK_FACEBOOK]
        tokens = [test_tokens.VK_ACCESS_TOKEN, test_tokens.GOOGLE_ACCESS_TOKEN, test_tokens.FACEBOOK_ACCESS_TOKEN]

        for network, access_token in zip(networks, tokens):
            resp = self.send_request(self.create_request_data(
                fields_values={
                    'name': self.VALID_TEST_ACCOUNT_NAME,
                    'access_token': ''
                },
            ), network=network, use_fake_ip=True)
            self.assert_error_code(resp, RegisterView.ERROR_SN_FETCH_DATA_ERROR)

            resp = self.send_request(self.create_request_data(
                fields_values={
                    'name': self.VALID_TEST_ACCOUNT_NAME,
                    'referrer': None,
                    'registrar': None,
                    'access_token': access_token
                },
            ), network=network, use_fake_ip=True)
            self.assert_resp_status(resp, 200)

            resp_data = resp.json()
            if 'error' in resp_data:
                self.assert_not_error_code(resp, RegisterView.ERROR_SN_FETCH_DATA_ERROR,
                                           "Can't fetch data from %s with provided access_token %s" % (
                                           network, access_token))

    def test_account_creation(self):
        resp = self.send_request(self.create_request_data(
            fields_values={
                'name': self.VALID_TEST_ACCOUNT_NAME,
                'referrer': None,
                'registrar': None,
                'access_token': test_tokens.VK_ACCESS_TOKEN
            },
        ), network=Account.NETWORK_VK, use_fake_ip=True)
        self.assert_resp_status(resp, 200)
        self.assertEqual('error' not in resp.json(), True, "Can't create account")


    def test_account_duplicate(self):
        self.test_account_creation()
        resp = self.send_request(self.create_request_data(
            fields_values={
                'name': self.VALID_TEST_ACCOUNT_NAME,
                'referrer': None,
                'registrar': None,
                'access_token': test_tokens.VK_ACCESS_TOKEN
            },
        ), network=Account.NETWORK_VK, use_fake_ip=True)
        self.assert_error_code(resp, RegisterView.ERROR_DUPLICATE_ACCOUNT)

