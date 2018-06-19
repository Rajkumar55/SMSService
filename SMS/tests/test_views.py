import base64
import json
from django.core.cache import cache
from django.contrib.auth.models import User
from rest_framework import status, HTTP_HEADER_ENCODING
from rest_framework.test import APITestCase


class SMSServiceTestCase(APITestCase):
    fixtures = ['sms.json']

    def setUp(self):
        self.test_user = User.objects.create_user('ben', password='123plivo!@#')
        self.valid_credentials = base64.b64encode('ben:123plivo!@#'.encode(HTTP_HEADER_ENCODING)).decode(HTTP_HEADER_ENCODING)

    def tearDown(self):
        self.test_user.delete()

    def test_inbound_sms_with_valid_data(self):
        headers = {'HTTP_AUTHORIZATION': 'Basic ' + self.valid_credentials}
        mock_data = {
            "from": "919876543210",
            "to": "919123456780",
            "text": "Hello Plivo"
        }
        response = self.client.post('/inbound/sms/', **headers, data=mock_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], 'inbound sms is ok')
        self.assertEqual(response_data['error'], '')
        # sms = SMS.objects.get(from_number=mock_data['from'], to_number=mock_data['to'])

    def test_inbound_sms_without_credentials(self):
        mock_data = {
            "from": "919876543210",
            "to": "919123456780",
            "text": "Hello Plivo"
        }
        response = self.client.post('/inbound/sms/', data=mock_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_inbound_sms_with_get_method(self):
        headers = {'HTTP_AUTHORIZATION': 'Basic ' + self.valid_credentials}
        response = self.client.get('/inbound/sms/', **headers)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_inbound_api_for_stop_sms(self):
        # Checking whether 'from' and 'to' are stored as key - value pair in Redis Cache for STOP sms text
        headers = {'HTTP_AUTHORIZATION': 'Basic ' + self.valid_credentials}
        mock_data = {
            "from": "919876543210",
            "to": "919123456780",
            "text": "STOP"
        }
        response = self.client.post('/inbound/sms/', **headers, data=mock_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], 'inbound sms is ok')
        self.assertEqual(response_data['error'], '')
        self.assertEqual(cache.get(mock_data['from']), mock_data['to'])

    def test_inbound_sms_with_missing_data(self):
        headers = {'HTTP_AUTHORIZATION': 'Basic ' + self.valid_credentials}
        mock_data = {
            "from": "919876543210",
            "text": "Hello Plivo"
        }
        response = self.client.post('/inbound/sms/', **headers, data=mock_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], '')
        self.assertEqual(response_data['error'], "'to' is missing")

    def test_inbound_sms_with_invalid_data(self):
        headers = {'HTTP_AUTHORIZATION': 'Basic ' + self.valid_credentials}
        mock_data = {
            "from": 'knklnlkn',
            "to": "919123456780",
            "text": "Hello Plivo"
        }
        response = self.client.post('/inbound/sms/', **headers, data=mock_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], '')
        self.assertEqual(response_data['error'], 'from is invalid')

    def test_outbound_sms_with_valid_data(self):
        headers = {'HTTP_AUTHORIZATION': 'Basic ' + self.valid_credentials}
        mock_data = {
            "from": "919944768524",
            "to": "919123456780",
            "text": "Hello Plivo"
        }
        response = self.client.post('/outbound/sms/', **headers, data=mock_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], 'outbound sms is ok')
        self.assertEqual(response_data['error'], '')

    def test_outbound_sms_without_credentials(self):
        mock_data = {
            "from": "919876543210",
            "to": "919123456780",
            "text": "Hello Plivo"
        }
        response = self.client.post('/outbound/sms/', data=mock_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_outbound_sms_with_put_method(self):
        headers = {'HTTP_AUTHORIZATION': 'Basic ' + self.valid_credentials}
        response = self.client.put('/outbound/sms/', **headers)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_outbound_api_for_stopped_number(self):
        headers = {'HTTP_AUTHORIZATION': 'Basic ' + self.valid_credentials}
        mock_data = {
            "from": "919123456780",
            "to": "919876543210",
            "text": "Good Morning"
        }
        response = self.client.post('/outbound/sms/', **headers, data=mock_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], '')
        self.assertEqual(response_data['error'], 'sms from 919123456780 and to 919876543210 blocked by STOP request')

    def test_outbound_sms_with_missing_data(self):
        headers = {'HTTP_AUTHORIZATION': 'Basic ' + self.valid_credentials}
        mock_data = {
            "to": "919944768524",
            "text": "Hello Plivo"
        }
        response = self.client.post('/outbound/sms/', **headers, data=mock_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], '')
        self.assertEqual(response_data['error'], "'from' is missing")

    def test_outbound_sms_with_invalid_data(self):
        headers = {'HTTP_AUTHORIZATION': 'Basic ' + self.valid_credentials}
        mock_data = {
            "from": '919876543210',
            "to": "kmkmkml",
            "text": "Hello Plivo"
        }
        response = self.client.post('/outbound/sms/', **headers, data=mock_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], '')
        self.assertEqual(response_data['error'], 'to is invalid')

    def test_outbound_sms_with_limit_reached(self):
        headers = {'HTTP_AUTHORIZATION': 'Basic ' + self.valid_credentials}
        mock_data = {
            "from": "919876543210",
            "to": "919123456780",
            "text": "Hello Plivo"
        }
        for i in range(0, 50):
            response = self.client.post('/outbound/sms/', **headers, data=mock_data, format='json')

        # Checking with more than 50 requests
        response = self.client.post('/outbound/sms/', **headers, data=mock_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], '')
        self.assertEqual(response_data['error'], 'limit reached for from 919876543210')
