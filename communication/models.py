from django.db import models

from core.models import SchoolScopedModel


class SmsTemplate(SchoolScopedModel):
    name = models.CharField(max_length=120)
    body = models.TextField()


class EmailTemplate(SchoolScopedModel):
    name = models.CharField(max_length=120)
    subject = models.CharField(max_length=200)
    body = models.TextField()


class NotificationTemplate(SchoolScopedModel):
    name = models.CharField(max_length=120)
    title = models.CharField(max_length=150)
    body = models.TextField()


class MessageLog(SchoolScopedModel):
    channel = models.CharField(max_length=20, choices=(("sms", "SMS"), ("email", "Email"), ("push", "Push")))
    recipient = models.CharField(max_length=120)
    message = models.TextField()
    status = models.CharField(max_length=20, default="queued")
    provider_response = models.TextField(blank=True)
