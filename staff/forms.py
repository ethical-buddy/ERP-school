from django import forms

from .models import Staff


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ["school", "employee_id", "first_name", "last_name", "department", "designation", "phone", "email", "is_active"]
