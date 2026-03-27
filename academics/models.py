from django.db import models

from core.models import AcademicSession, SchoolScopedModel
from staff.models import Staff


class Course(SchoolScopedModel):
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=30)

    class Meta:
        unique_together = ("school", "code")

    def __str__(self):
        return self.name


class Section(SchoolScopedModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="sections")
    name = models.CharField(max_length=50)

    class Meta:
        unique_together = ("course", "name")

    def __str__(self):
        return f"{self.course.name} - {self.name}"


class Subject(SchoolScopedModel):
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=30)

    class Meta:
        unique_together = ("school", "code")

    def __str__(self):
        return self.name


class TimetableSlot(SchoolScopedModel):
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day_of_week = models.PositiveSmallIntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        indexes = [models.Index(fields=["school", "day_of_week"])]


class ClassTeacherAssignment(SchoolScopedModel):
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("school", "session", "course", "section")

    def __str__(self):
        return f"{self.course} {self.section} -> {self.staff.first_name}"


class SubjectTeacherAssignment(SchoolScopedModel):
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("school", "session", "course", "section", "subject")

    def __str__(self):
        return f"{self.course} {self.section} {self.subject} -> {self.staff.first_name}"
