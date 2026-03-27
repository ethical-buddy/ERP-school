from datetime import date

from django.contrib.auth.models import Group, User
from django.test import Client, TestCase

from accounts.models import UserProfile
from academics.models import ClassTeacherAssignment, Course, Section
from core.models import AcademicSession, School
from staff.models import Department, Designation, Staff
from students.models import Student

from .models import StudentAttendance


class ClassTeacherAttendanceTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.school = School.objects.create(name="S", code="S")
        self.session = AcademicSession.objects.create(school=self.school, title="2026-27", start_date="2026-04-01", end_date="2027-03-31", is_active=True)
        self.course = Course.objects.create(school=self.school, name="Class 10", code="10")
        self.section = Section.objects.create(school=self.school, course=self.course, name="A")
        dept = Department.objects.create(school=self.school, name="Academics")
        desg = Designation.objects.create(school=self.school, name="Teacher")
        self.staff = Staff.objects.create(school=self.school, employee_id="EMP1", first_name="T", department=dept, designation=desg)
        self.student = Student.objects.create(school=self.school, admission_no="ADM1", first_name="Ria", course=self.course, section=self.section)

        teacher_group, _ = Group.objects.get_or_create(name="teacher_portal")
        self.teacher_user = User.objects.create_user(username="t", password="StrongPass@12345")
        self.teacher_user.groups.add(teacher_group)
        UserProfile.objects.create(user=self.teacher_user, school=self.school, staff=self.staff)

        ClassTeacherAssignment.objects.create(
            school=self.school,
            session=self.session,
            course=self.course,
            section=self.section,
            staff=self.staff,
            is_active=True,
        )

    def test_teacher_can_mark_attendance(self):
        self.client.login(username="t", password="StrongPass@12345")
        assignment = ClassTeacherAssignment.objects.first()
        response = self.client.post(
            "/attendance/class-teacher/",
            {
                "assignment_id": assignment.id,
                "attendance_date": str(date.today()),
                f"status_{self.student.id}": "A",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(StudentAttendance.objects.filter(student=self.student).count(), 1)
        self.assertEqual(StudentAttendance.objects.get(student=self.student).status, "A")
