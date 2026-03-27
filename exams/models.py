from django.conf import settings
from django.db import models

from academics.models import Course, Section, Subject
from core.models import SchoolScopedModel
from students.models import Student


class ExamType(SchoolScopedModel):
    name = models.CharField(max_length=120)


class ExamTerm(SchoolScopedModel):
    name = models.CharField(max_length=120)


class Exam(SchoolScopedModel):
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE)
    exam_term = models.ForeignKey(ExamTerm, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_date = models.DateField()
    max_marks = models.DecimalField(max_digits=6, decimal_places=2)


class ExamComponent(SchoolScopedModel):
    COMPONENT_CHOICES = (("theory", "Theory"), ("internal", "Internal"), ("practical", "Practical"))
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="components")
    component_type = models.CharField(max_length=20, choices=COMPONENT_CHOICES)
    max_marks = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ("school", "exam", "component_type")


class MarkRecord(SchoolScopedModel):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=6, decimal_places=2)
    remarks = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ("school", "exam", "student")


class StudentExamComponentMark(SchoolScopedModel):
    record = models.ForeignKey(MarkRecord, on_delete=models.CASCADE, related_name="component_marks")
    component = models.ForeignKey(ExamComponent, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=6, decimal_places=2)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ("school", "record", "component")
