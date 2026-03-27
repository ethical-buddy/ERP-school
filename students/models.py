from django.db import models

from academics.models import Course, Section
from core.models import SchoolScopedModel


class Student(SchoolScopedModel):
    admission_no = models.CharField(max_length=40)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.SET_NULL)
    section = models.ForeignKey(Section, null=True, blank=True, on_delete=models.SET_NULL)
    guardian_name = models.CharField(max_length=120, blank=True)
    guardian_phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("school", "admission_no")
        indexes = [models.Index(fields=["school", "first_name"])]

    def __str__(self):
        return f"{self.admission_no} - {self.first_name}"


class ProspectusLead(SchoolScopedModel):
    enquiry_no = models.CharField(max_length=40)
    student_name = models.CharField(max_length=120)
    contact_phone = models.CharField(max_length=20)
    interested_course = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=40, default="new")


class StudentDocumentType(SchoolScopedModel):
    name = models.CharField(max_length=120)


class StudentDocument(SchoolScopedModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="documents")
    document_type = models.ForeignKey(StudentDocumentType, on_delete=models.CASCADE)
    file = models.FileField(upload_to="student_documents/")


class IDCardTemplate(SchoolScopedModel):
    name = models.CharField(max_length=120)
    front_html = models.TextField(blank=True)
    back_html = models.TextField(blank=True)


class CertificateTemplate(SchoolScopedModel):
    name = models.CharField(max_length=120)
    body_html = models.TextField()


class StudentCertificate(SchoolScopedModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    template = models.ForeignKey(CertificateTemplate, on_delete=models.CASCADE)
    issue_date = models.DateField()
    certificate_no = models.CharField(max_length=40)

    class Meta:
        unique_together = ("school", "certificate_no")
