from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

from accounts.models import UserProfile
from core.models import School
from students.models import Student


class APISmokeTests(APITestCase):
    def setUp(self):
        self.school = School.objects.create(name="S1", code="S1")
        self.user = User.objects.create_user(username="apiuser", password="StrongPass@12345")
        UserProfile.objects.create(user=self.user, school=self.school)

    def auth(self):
        response = self.client.post(reverse("token_obtain_pair"), {"username": "apiuser", "password": "StrongPass@12345"}, format="json")
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_health_requires_auth(self):
        response = self.client.get(reverse("api-health"))
        self.assertEqual(response.status_code, 401)

    def test_auth_and_me(self):
        self.auth()
        response = self.client.get(reverse("api-me"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], "apiuser")

    def test_student_list(self):
        Student.objects.create(school=self.school, admission_no="A1", first_name="Ria")
        self.auth()
        response = self.client.get("/api/v1/students/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
