from rest_framework import serializers
from SMS.serializers import SMSSerializer
from django.core.cache import cache
from django.conf import settings


def save_inbound_sms(data):
    response = {}
    try:
        text = data['text']
        sms_data = {
            'from_number': data['from'],
            'to_number': data['to'],
            'text': data['text'],
            'message_type': 1  # Marking it as Inbound SMS
        }
        serializer = SMSSerializer(data=sms_data)
        is_valid = serializer.is_valid(raise_exception=True)  # Validating the input params
        if is_valid:
            serializer.save()  # Save in DataBase
            # If the text is STOP, store the from and to pair in cache with TTL value as 4 hours
            if text in ['STOP', 'STOP\n', 'STOP\r', 'STOP\r\n']:
                cache.set(data['from'], data['to'], timeout=settings.CACHE_TTL)
            response['message'] = 'inbound sms is ok'
            response['error'] = ''
            response_status_code = 200
    
        else:
            response['message'] = ''
            response['error'] = 'unknown failure'
            response_status_code = 400

    except KeyError as ke:
        response['message'] = ''
        response['error'] = '{} is missing'.format(ke)
        response_status_code = 400
    
    except ValueError as ve:
        response['message'] = ''
        response['error'] = str(ve)
        response_status_code = 400
    
    except Exception as e:
        print(e)
        response['message'] = ''
        response['error'] = 'unknown failure'
        response_status_code = 400
    
    return response, response_status_code


def save_outbound_sms(data):
    response = {}
    try:
        text = data['text']
        sms_data = {
            'from_number': data['from'],
            'to_number': data['to'],
            'text': text,
            'message_type': 2  # Marking it as Outbound SMS
        }
        serializer = SMSSerializer(data=sms_data)
        is_valid = serializer.is_valid(raise_exception=True)
        if is_valid:
            limit_cache_key = 'limit_' + data['from']
            limit = 1
            if cache.get(limit_cache_key):  # Check cache for requests limit
                limit = cache.get(limit_cache_key) + 1
                # If requests limit from the same number reaches above 50, do not allow
                if cache.get(limit_cache_key) >= 50:
                    response['message'] = ''
                    response['error'] = 'limit reached for from {}'.format(data['from'])
                    return response, 400

            if cache.get(data['to']) == data['from']:
                response['message'] = ''
                response['error'] = 'sms from {from_number} and to {to_number} blocked by STOP request'.format(
                    from_number=data['from'], to_number=data['to'])
                response_status_code = 400

            else:
                # Set the requests limit for the from number with TTL as 1 hour
                cache.set(limit_cache_key, limit, timeout=60 * 60)

                serializer.save()  # Save in DataBase
                response['message'] = 'outbound sms is ok'
                response['error'] = ''
                response_status_code = 200

        else:
            response['message'] = ''
            response['error'] = 'unknown failure'
            response_status_code = 400

    except KeyError as ke:
        response['message'] = ''
        response['error'] = '{} is missing'.format(ke)
        response_status_code = 400

    except ValueError as ve:
        response['message'] = ''
        response['error'] = str(ve)
        response_status_code = 400

    except Exception as e:
        print(e)
        response['message'] = ''
        response['error'] = 'unknown failure'
        response_status_code = 400

    return response, response_status_code
