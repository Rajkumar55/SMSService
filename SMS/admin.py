from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from SMS.models import SMS


@admin.register(SMS)
class SMSAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    search_fields = ['from_number', 'to_number']
    list_display = ['id', 'from_number', 'to_number', 'text', 'message_type', 'created_date']
    list_filter = ['message_type']
