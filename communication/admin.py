from django.contrib import admin

from .models import EmailTemplate, MessageLog, NotificationTemplate, SmsTemplate

admin.site.register(SmsTemplate)
admin.site.register(EmailTemplate)
admin.site.register(NotificationTemplate)
admin.site.register(MessageLog)
