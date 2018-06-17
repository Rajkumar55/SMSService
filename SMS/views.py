import json

from django.http import JsonResponse
from django.views import View
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from SMS.serializers import SMSSerializer


class InboundSMS(viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        try:
            request_body = json.loads(request.body)
            data = {
                'from_number': request_body['from'],
                'to_number': request_body['to'],
                'text': request_body['text'],
                'message_type': 1  # Marking it as Inbound SMS
            }
            serializer = SMSSerializer(data=data)
            is_valid = serializer.is_valid(raise_exception=True)
            if is_valid:
                serializer.save()
                return JsonResponse({'message': 'inbound sms is ok', 'error': ''})

            else:
                return JsonResponse({'message': '', 'error': serializer.errors})

        except KeyError as ke:
            return JsonResponse({'message': '', 'error': '{} is missing'.format(ke)})

        except ValueError as ve:
            return JsonResponse({'message': '', 'error': str(ve)})

        except Exception as e:
            print('dvdvcv')
            return JsonResponse({'message': 'error', 'error': str(e)})
