from django import forms

from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "school",
            "admission_no",
            "first_name",
            "last_name",
            "dob",
            "gender",
            "course",
            "section",
            "guardian_name",
            "guardian_phone",
            "address",
            "is_active",
        ]
