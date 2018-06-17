from django.urls import path
from SMS.views import InboundSMS

inbound_sms = InboundSMS.as_view({
    'post': 'create'
})
urlpatterns = [
    path('inbound/sms/', inbound_sms)
]
