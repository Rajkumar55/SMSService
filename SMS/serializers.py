from rest_framework import serializers
from .models import *


class SMSSerializer(serializers.Serializer):
    from_number = serializers.CharField()
    to_number = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    text = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    message_type = serializers.ChoiceField(choices=MESSAGE_TYPES, default=1, allow_null=False, allow_blank=False)

    def validate(self, attrs):
        if len(attrs['from_number']) < 6 or len(attrs['from_number']) > 16 or not attrs['from_number'].isdigit():
            raise ValueError('from is invalid')
        if len(attrs['to_number']) < 6 or len(attrs['to_number']) > 16 or not attrs['to_number'].isdigit():
            raise ValueError('to is invalid')
        if len(attrs['text']) == 0 or len(attrs['text']) > 120:
            raise ValueError('text is invalid')
        return attrs

    def create(self, validated_data):
        sms = SMS()
        sms.from_number = validated_data.get('from_number')
        sms.to_number = validated_data.get('to_number')
        sms.text = validated_data.get('text')
        sms.message_type = validated_data.get('message_type')
        sms.save()
        return sms
