from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework.test import APITestCase

from accounts.models import UserProfile
from core.models import AuditLog, School
from finance.models import FeeHead
from transport.models import Route
from students.models import Student


class APISmokeTests(APITestCase):
    def setUp(self):
        self.school = School.objects.create(name="S1", code="S1")
        self.user = User.objects.create_user(username="apiuser", password="StrongPass@12345")
        UserProfile.objects.create(user=self.user, school=self.school)
        Group.objects.get_or_create(name="api_manager")

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
        health_response = self.client.get(reverse("api-health"))
        self.assertEqual(health_response.status_code, 200)
        self.assertEqual(health_response.data["database"], "ok")
        readiness_response = self.client.get(reverse("api-readiness"))
        self.assertEqual(readiness_response.status_code, 200)
        self.assertTrue(readiness_response.data["ready"])

    def test_student_list(self):
        Student.objects.create(school=self.school, admission_no="A1", first_name="Ria")
        self.auth()
        response = self.client.get("/api/v1/students/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_write_requires_manager_role(self):
        self.auth()
        response = self.client.post("/api/v1/students/", {"admission_no": "A2", "first_name": "NoRole"}, format="json")
        self.assertEqual(response.status_code, 403)

    def test_transport_route_list(self):
        Route.objects.create(school=self.school, name="North Route", code="NR-1")
        self.auth()
        response = self.client.get("/api/v1/transport/routes/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_phase3_module_endpoints_available(self):
        self.auth()
        endpoints = [
            "/api/v1/academics/courses/",
            "/api/v1/finance/fee-heads/",
            "/api/v1/library/books/",
            "/api/v1/exams/types/",
            "/api/v1/inventory/items/",
            "/api/v1/communication/sms-templates/",
            "/api/v1/frontoffice/visitors/",
        ]
        for endpoint in endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(response.status_code, 200)

    def test_phase4_audit_log_written_on_create(self):
        manager_group = Group.objects.get(name="api_manager")
        self.user.groups.add(manager_group)
        self.auth()
        response = self.client.post("/api/v1/finance/fee-heads/", {"name": "Tuition"}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(FeeHead.objects.count(), 1)
        self.assertEqual(AuditLog.objects.filter(action="create", entity="FeeHead").count(), 1)
