from django.contrib.auth.models import Group, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from academics.models import Course, Section, Subject
from accounts.models import UserProfile
from core.models import AcademicSession, School
from staff.models import Department, Designation, Staff
from students.models import Student

from .models import Exam, ExamComponent, ExamTerm, ExamType, MarkRecord, StudentExamComponentMark


class ExamUploadTests(TestCase):
    def setUp(self):
        self.school = School.objects.create(name="Demo", code="D1")
        self.session = AcademicSession.objects.create(school=self.school, title="2026-27", start_date="2026-04-01", end_date="2027-03-31")
        self.course = Course.objects.create(school=self.school, code="10", name="Class 10")
        self.section = Section.objects.create(school=self.school, course=self.course, name="A")
        self.subject = Subject.objects.create(school=self.school, code="MATH", name="Mathematics")
        self.exam_type = ExamType.objects.create(school=self.school, name="Unit Test")
        self.exam_term = ExamTerm.objects.create(school=self.school, name="Term 1")

        dept = Department.objects.create(school=self.school, name="Academics")
        desg = Designation.objects.create(school=self.school, name="Teacher")
        self.staff = Staff.objects.create(school=self.school, employee_id="E1", first_name="Teach", department=dept, designation=desg)

        self.student = Student.objects.create(school=self.school, admission_no="ADM1", first_name="Ria", course=self.course, section=self.section)

        self.exam = Exam.objects.create(
            school=self.school,
            exam_type=self.exam_type,
            exam_term=self.exam_term,
            course=self.course,
            section=self.section,
            subject=self.subject,
            exam_date="2026-09-20",
            max_marks=100,
        )
        ExamComponent.objects.create(school=self.school, exam=self.exam, component_type="theory", max_marks=70)
        ExamComponent.objects.create(school=self.school, exam=self.exam, component_type="internal", max_marks=20)
        ExamComponent.objects.create(school=self.school, exam=self.exam, component_type="practical", max_marks=10)

        self.teacher_group, _ = Group.objects.get_or_create(name="teacher_portal")
        self.student_group, _ = Group.objects.get_or_create(name="student_portal")

        self.teacher_user = User.objects.create_user(username="teacher", password="StrongPass@12345")
        self.teacher_user.groups.add(self.teacher_group)
        UserProfile.objects.create(user=self.teacher_user, school=self.school, staff=self.staff)

        self.student_user = User.objects.create_user(username="student", password="StrongPass@12345")
        self.student_user.groups.add(self.student_group)
        UserProfile.objects.create(user=self.student_user, school=self.school, student=self.student)

    def test_teacher_can_upload_marks(self):
        self.client.login(username="teacher", password="StrongPass@12345")
        payload = b"admission_no,theory,internal,practical,remarks\nADM1,61,17,8,Good"
        file = SimpleUploadedFile("marks.csv", payload, content_type="text/csv")
        response = self.client.post("/exams/bulk-upload/", {"exam": self.exam.id, "marks_file": file})
        self.assertEqual(response.status_code, 302)
        record = MarkRecord.objects.get(student=self.student, exam=self.exam)
        self.assertEqual(float(record.marks_obtained), 86.0)
        self.assertEqual(StudentExamComponentMark.objects.filter(record=record).count(), 3)

    def test_student_cannot_open_exam_upload(self):
        self.client.login(username="student", password="StrongPass@12345")
        response = self.client.get("/exams/bulk-upload/")
        self.assertEqual(response.status_code, 403)
