from django.test import TestCase


class ApiTestCase(TestCase):
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

    def assert_api_success(self, resp, msg=None):
        if msg is None:
            msg = 'Result of this operation must be success'

        self.assert_resp_status(resp, 200, msg)
        self.assertEqual('error' not in resp.json(), True, msg)