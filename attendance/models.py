from django.db import models

from academics.models import Course, Section
from core.models import SchoolScopedModel
from staff.models import Staff
from students.models import Student


class Holiday(SchoolScopedModel):
    title = models.CharField(max_length=120)
    date = models.DateField()


class LeaveType(SchoolScopedModel):
    name = models.CharField(max_length=120)
    max_days = models.PositiveIntegerField(default=0)


class StudentAttendance(SchoolScopedModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.SET_NULL)
    section = models.ForeignKey(Section, null=True, blank=True, on_delete=models.SET_NULL)
    attendance_date = models.DateField()
    status = models.CharField(max_length=10, choices=(("P", "Present"), ("A", "Absent"), ("L", "Leave")))

    class Meta:
        unique_together = ("school", "student", "attendance_date")
        indexes = [models.Index(fields=["school", "attendance_date"])]


class StaffAttendance(SchoolScopedModel):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    attendance_date = models.DateField()
    status = models.CharField(max_length=10, choices=(("P", "Present"), ("A", "Absent"), ("L", "Leave")))

    class Meta:
        unique_together = ("school", "staff", "attendance_date")


class LeaveRequest(SchoolScopedModel):
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, null=True, blank=True, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, null=True, blank=True, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, default="pending")
