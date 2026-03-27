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


class MarkRecord(SchoolScopedModel):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=6, decimal_places=2)
    remarks = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ("school", "exam", "student")
