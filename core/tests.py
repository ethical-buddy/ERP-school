from django.contrib.auth.models import User
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


class SchoolModelTests(TestCase):
    def test_school_creation(self):
        school = School.objects.create(name="My School", code="MS")
        self.assertEqual(str(school), "My School")
