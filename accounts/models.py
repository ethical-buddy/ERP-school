from django.conf import settings
from django.db import models

from core.models import School, SchoolBranch, SchoolScopedModel


class UserProfile(SchoolScopedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    branch = models.ForeignKey(SchoolBranch, null=True, blank=True, on_delete=models.SET_NULL)
    student = models.OneToOneField("students.Student", null=True, blank=True, on_delete=models.SET_NULL, related_name="portal_profile")
    staff = models.OneToOneField("staff.Staff", null=True, blank=True, on_delete=models.SET_NULL, related_name="portal_profile")
    phone = models.CharField(max_length=20, blank=True)
    designation = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return self.user.get_username()
