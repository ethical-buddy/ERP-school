from django.db import models

from core.models import SchoolScopedModel
from students.models import Student


class Visitor(SchoolScopedModel):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20, blank=True)
    purpose = models.CharField(max_length=200)
    visit_date = models.DateField()


class Enquiry(SchoolScopedModel):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    query = models.TextField()
    status = models.CharField(max_length=30, default="open")


class Complaint(SchoolScopedModel):
    raised_by = models.CharField(max_length=120)
    complaint_type = models.CharField(max_length=120)
    detail = models.TextField()
    status = models.CharField(max_length=30, default="open")


class Appointment(SchoolScopedModel):
    person_name = models.CharField(max_length=120)
    appointment_for = models.CharField(max_length=120)
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=30, default="scheduled")


class GatePass(SchoolScopedModel):
    student = models.ForeignKey(Student, null=True, blank=True, on_delete=models.SET_NULL)
    issued_to = models.CharField(max_length=120)
    reason = models.CharField(max_length=255)
    issue_date = models.DateField()


class ServiceRequest(SchoolScopedModel):
    requester = models.CharField(max_length=120)
    title = models.CharField(max_length=120)
    detail = models.TextField()
    status = models.CharField(max_length=30, default="new")
