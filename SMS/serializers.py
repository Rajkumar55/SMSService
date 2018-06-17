from rest_framework import serializers
from .models import *


class SMSSerializer(serializers.Serializer):
    from_number = serializers.CharField()
    to_number = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    text = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    message_type = serializers.ChoiceField(choices=MESSAGE_TYPES, default=1, allow_null=False, allow_blank=False)

    def __init__(self, *args, **kwargs):
        super(SMSSerializer, self).__init__(*args, **kwargs)

        self.fields['from_number'].error_messages['invalid'] = 'My custom required msg'

    def validate(self, attrs):
        # error_count = 0
        # err_value = ''
        # for key, value in attrs.items():
        #     if value in ['from_number', 'to_number']:
        #         if len(value) < 6 or len(value) > 16:
        #             print('Error ' + value)
        #             error_count += 1
        #             err_value = key
        #             break
        #
        # if error_count:
        #     raise ValueError('{} is invalid'.format(err_value))
        if len(attrs['from_number']) < 6 or len(attrs['from_number']) > 16:
            raise ValueError('from is invalid')
        if len(attrs['to_number']) < 6 or len(attrs['to_number']) > 16:
            raise ValueError('to is invalid')
        return attrs

    def create(self, validated_data):
        sms = SMS()
        sms.from_number = validated_data.get('from_number')
        sms.to_number = self.initial_data.get('to_number')
        sms.text = self.initial_data.get('text')
        sms.message_type = self.initial_data.get('message_type')
        sms.save()
        return sms
