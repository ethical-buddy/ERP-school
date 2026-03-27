from django.db import models

from core.models import SchoolScopedModel


class Department(SchoolScopedModel):
    name = models.CharField(max_length=120)


class Designation(SchoolScopedModel):
    name = models.CharField(max_length=120)


class Staff(SchoolScopedModel):
    employee_id = models.CharField(max_length=40)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120, blank=True)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)
    designation = models.ForeignKey(Designation, null=True, blank=True, on_delete=models.SET_NULL)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("school", "employee_id")


class StaffDocumentType(SchoolScopedModel):
    name = models.CharField(max_length=120)
