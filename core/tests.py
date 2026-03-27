from django.contrib.auth.models import Group, User
from django.test import Client, TestCase
from django.urls import reverse

from core.models import School


class DashboardTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="u1", password="StrongPass@12345")

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_loads_for_authenticated_user(self):
        self.client.login(username="u1", password="StrongPass@12345")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("X-Response-Time-Ms", response.headers)


class SchoolModelTests(TestCase):
    def test_school_creation(self):
        school = School.objects.create(name="My School", code="MS")
        self.assertEqual(str(school), "My School")


class PortalTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher_group, _ = Group.objects.get_or_create(name="teacher_portal")
        self.student_group, _ = Group.objects.get_or_create(name="student_portal")
        self.admin = User.objects.create_superuser(username="a1", password="StrongPass@12345", email="a1@example.com")
        self.teacher = User.objects.create_user(username="t1", password="StrongPass@12345")
        self.teacher.groups.add(self.teacher_group)
        self.student = User.objects.create_user(username="s1", password="StrongPass@12345")
        self.student.groups.add(self.student_group)

    def test_post_login_router_admin(self):
        self.client.login(username="a1", password="StrongPass@12345")
        response = self.client.get(reverse("post_login"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/portal/admin/", response.url)

    def test_post_login_router_teacher(self):
        self.client.login(username="t1", password="StrongPass@12345")
        response = self.client.get(reverse("post_login"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/portal/teacher/", response.url)

    def test_student_cannot_open_admin_portal(self):
        self.client.login(username="s1", password="StrongPass@12345")
        response = self.client.get(reverse("admin_portal"))
        self.assertEqual(response.status_code, 403)

    def test_student_cannot_open_finance_or_attendance(self):
        self.client.login(username="s1", password="StrongPass@12345")
        finance_response = self.client.get("/finance/")
        attendance_response = self.client.get("/attendance/")
        self.assertEqual(finance_response.status_code, 403)
        self.assertEqual(attendance_response.status_code, 403)
