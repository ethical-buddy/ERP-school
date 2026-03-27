from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from academics.models import Course, Section
from core.models import AcademicSession, FeatureFlag, FinancialYear, School, SchoolBranch, SchoolFeature


class Command(BaseCommand):
    help = "Seed minimum demo data"

    def handle(self, *args, **options):
        school, _ = School.objects.get_or_create(code="DEMO", defaults={"name": "Demo School"})
        SchoolBranch.objects.get_or_create(school=school, code="MAIN", defaults={"name": "Main Branch"})
        AcademicSession.objects.get_or_create(
            school=school,
            title="2026-27",
            defaults={"start_date": "2026-04-01", "end_date": "2027-03-31", "is_active": True},
        )
        FinancialYear.objects.get_or_create(
            school=school,
            title="FY 2026-27",
            defaults={"start_date": "2026-04-01", "end_date": "2027-03-31", "is_active": True},
        )

        features = [
            "students",
            "staff",
            "attendance",
            "finance",
            "transport",
            "library",
            "exams",
            "inventory",
            "communication",
            "frontoffice",
            "academics",
        ]
        for slug in features:
            flag, _ = FeatureFlag.objects.get_or_create(slug=slug, defaults={"name": slug.title()})
            SchoolFeature.objects.get_or_create(school=school, feature=flag, defaults={"is_enabled": True})

        course, _ = Course.objects.get_or_create(school=school, code="10", defaults={"name": "Class 10"})
        Section.objects.get_or_create(school=school, course=course, name="A")

        user_model = get_user_model()
        if not user_model.objects.filter(username="admin").exists():
            user_model.objects.create_superuser("admin", "admin@example.com", "Admin@12345678")

        self.stdout.write(self.style.SUCCESS("Demo data seeded. Username: admin Password: Admin@12345678"))
