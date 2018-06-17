from django.urls import path
from SMS.views import InboundSMS, OutboundSMS

inbound_sms = InboundSMS.as_view({
    'post': 'create'
})

outbound_sms = OutboundSMS.as_view({
    'post': 'create'
})

urlpatterns = [
    path('inbound/sms/', inbound_sms),
    path('outbound/sms/', outbound_sms)
]
