from django.test import TestCase
from SMS.controllers import save_inbound_sms, save_outbound_sms
from SMS.models import SMS
from django.core.cache import cache


class URLInfoTestCase(TestCase):
    fixtures = ['sms.json']

    def test_save_inbound_sms_with_valid_data(self):
        mock_data = {
            "from": "919876543210",
            "to": "919123456780",
            "text": "Hello Plivo"
        }

        response, status_code = save_inbound_sms(mock_data)
        self.assertEqual(status_code, 200)
        self.assertEqual(response['message'], 'inbound sms is ok')
        self.assertEqual(response['error'], '')

    def test_save_inbound_sms_with_redis(self):
        mock_data = {
            "from": "919876543210",
            "to": "919123456780",
            "text": "STOP"
        }

        response, status_code = save_inbound_sms(mock_data)
        self.assertEqual(status_code, 200)
        self.assertEqual(response['message'], 'inbound sms is ok')
        self.assertEqual(response['error'], '')
        # Check whether the from and to are stored in Redis Cache
        self.assertEqual(cache.get(mock_data['from']), mock_data['to'])

    def test_save_inbound_sms_with_missing_data(self):
        mock_data = {
            "to": "919123456780",
            "text": "Hello Plivo"
        }

        response, status_code = save_inbound_sms(mock_data)
        self.assertEqual(status_code, 400)
        self.assertEqual(response['message'], '')
        self.assertEqual(response['error'], "'from' is missing")

    def test_save_inbound_sms_with_invalid_data(self):
        mock_data = {
            "from": "12345",
            "to": "919123456780",
            "text": "Hello Plivo"
        }

        response, status_code = save_inbound_sms(mock_data)
        self.assertEqual(status_code, 400)
        self.assertEqual(response['message'], '')
        self.assertEqual(response['error'], "from is invalid")

    def test_save_outbound_sms_with_valid_data(self):
        mock_data = {
            "from": "919876543210",
            "to": "919123456780",
            "text": "Hello Plivo"
        }

        response, status_code = save_outbound_sms(mock_data)
        self.assertEqual(status_code, 200)
        self.assertEqual(response['message'], 'outbound sms is ok')
        self.assertEqual(response['error'], '')

    def test_save_outbound_sms_with_missing_data(self):
        mock_data = {
            "from": "919876543210",
            "text": "Hello Plivo"
        }

        response, status_code = save_outbound_sms(mock_data)
        self.assertEqual(status_code, 400)
        self.assertEqual(response['message'], '')
        self.assertEqual(response['error'], "'to' is missing")

    def test_save_outbound_sms_with_invalid_data(self):
        mock_data = {
            "from": "919876543210",
            "to": "test",
            "text": "Hello Plivo"
        }

        response, status_code = save_inbound_sms(mock_data)
        self.assertEqual(status_code, 400)
        self.assertEqual(response['message'], '')
        self.assertEqual(response['error'], "to is invalid")

    def test_save_outbound_sms_for_stop_number(self):
        mock_data = {
            "from": "919123456780",
            "to": "919876543210",
            "text": "Hello Plivo"
        }

        response, status_code = save_outbound_sms(mock_data)
        self.assertEqual(status_code, 400)
        self.assertEqual(response['message'], '')
        self.assertEqual(response['error'], 'sms from {from_number} and to {to_number} blocked by STOP request'.format(
                        from_number=mock_data['from'], to_number=mock_data['to']))
