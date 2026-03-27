from django import forms

from .models import StudentAttendance


class StudentAttendanceForm(forms.ModelForm):
    class Meta:
        model = StudentAttendance
        fields = ["school", "student", "course", "section", "attendance_date", "status"]
