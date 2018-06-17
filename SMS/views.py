import json
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from SMS.controllers import save_inbound_sms, save_outbound_sms


class InboundSMS(viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication,)  # Authenticating the API via REST Framework's Basic Authentication
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        request_body = json.loads(request.body)
        response, status_code = save_inbound_sms(request_body)
        return JsonResponse(response, status=status_code)


class OutboundSMS(viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication,)  # Authenticating the API via Basic Authentication
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        request_body = json.loads(request.body)
        response, status_code = save_outbound_sms(request_body)
        return JsonResponse(response, status=status_code)
