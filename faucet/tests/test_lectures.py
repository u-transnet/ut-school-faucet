from django.test import override_settings, TestCase

from faucet.models import Account


@override_settings(BLOCKCHAIN_NOBROADCAST=True)
class RegistrationTest(TestCase):
    FAKE_IP = '192.168.0.15'
    DEFAULT_NETWORK = Account.NETWORK_VK

    VALID_TEST_ACCOUNT_NAME = 'test_account23'
    VALID_TEST_ACCOUNT_SECOND_NAME = 'test_account22'
    PRIMARY_ACCOUNT_NAME = 'test_account'
    EXISTS_ACCOUNT_NAME = 'u-tech-faucet'