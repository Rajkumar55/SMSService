from django.db import models

MESSAGE_TYPES = (
    (1, 'inbound'),
    (2, 'outbound')
)


class SMS(models.Model):
    from_number = models.CharField(max_length=16, null=False, blank=False)
    to_number = models.CharField(max_length=16, null=False, blank=False)
    text = models.CharField(max_length=120, null=False, blank=False, help_text='SMS Text')
    message_type = models.IntegerField(default=1, choices=MESSAGE_TYPES, null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
