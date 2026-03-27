from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from accounts.models import UserProfile
from academics.models import ClassTeacherAssignment, Course, Section, Subject, SubjectTeacherAssignment
from attendance.models import LeaveRequest, LeaveType, StaffAttendance, StudentAttendance
from core.models import AcademicSession, FinancialYear, School, SchoolBranch
from finance.models import ExpenseCategory, ExpenseEntry, FeeHead, FeeInvoice
from staff.models import Department, Designation, Staff
from students.models import Student


class Command(BaseCommand):
    help = "Seed sample users and ERP records for portal testing"

    def handle(self, *args, **options):
        school, _ = School.objects.get_or_create(code="DEMO", defaults={"name": "Demo School"})
        branch, _ = SchoolBranch.objects.get_or_create(school=school, code="MAIN", defaults={"name": "Main Branch"})
        session, _ = AcademicSession.objects.get_or_create(
            school=school,
            title="2026-27",
            defaults={"start_date": "2026-04-01", "end_date": "2027-03-31", "is_active": True},
        )
        FinancialYear.objects.get_or_create(
            school=school,
            title="FY 2026-27",
            defaults={"start_date": "2026-04-01", "end_date": "2027-03-31", "is_active": True},
        )

        for code in ["PLAY", "NUR", "LKG", "UKG"] + [str(i) for i in range(1, 13)]:
            Course.objects.get_or_create(school=school, code=code, defaults={"name": f"Class {code}" if code.isdigit() else code})

        admin_group, _ = Group.objects.get_or_create(name="admin_portal")
        teacher_group, _ = Group.objects.get_or_create(name="teacher_portal")
        student_group, _ = Group.objects.get_or_create(name="student_portal")
        api_group, _ = Group.objects.get_or_create(name="api_manager")

        from django.contrib.auth import get_user_model

        User = get_user_model()
        admin_user, _ = User.objects.get_or_create(username="admin_demo", defaults={"email": "admin.demo@schoolerp.local", "is_superuser": True, "is_staff": True})
        admin_user.set_password("Admin@12345678")
        admin_user.is_superuser = True
        admin_user.is_staff = True
        admin_user.save()
        admin_user.groups.add(admin_group, api_group)

        teacher_user, _ = User.objects.get_or_create(username="teacher_demo", defaults={"email": "teacher.demo@schoolerp.local", "is_staff": True})
        teacher_user.set_password("Teacher@12345678")
        teacher_user.is_staff = True
        teacher_user.save()
        teacher_user.groups.add(teacher_group)

        student_user, _ = User.objects.get_or_create(username="student_demo", defaults={"email": "student.demo@schoolerp.local"})
        student_user.set_password("Student@12345678")
        student_user.save()
        student_user.groups.add(student_group)

        UserProfile.objects.get_or_create(user=admin_user, defaults={"school": school, "branch": branch, "designation": "System Administrator"})

        course10, _ = Course.objects.get_or_create(school=school, code="10", defaults={"name": "Class 10"})
        course9, _ = Course.objects.get_or_create(school=school, code="9", defaults={"name": "Class 9"})
        sec_a, _ = Section.objects.get_or_create(school=school, course=course10, name="A")
        sec_b, _ = Section.objects.get_or_create(school=school, course=course9, name="B")

        dept, _ = Department.objects.get_or_create(school=school, name="Academics")
        desg, _ = Designation.objects.get_or_create(school=school, name="TGT")

        staff_record, _ = Staff.objects.get_or_create(
            school=school,
            employee_id="EMP1001",
            defaults={
                "first_name": "Aarav",
                "last_name": "Sharma",
                "department": dept,
                "designation": desg,
                "phone": "9990001111",
                "email": "teacher.demo@schoolerp.local",
                "is_active": True,
            },
        )

        teacher_profile, _ = UserProfile.objects.get_or_create(user=teacher_user, defaults={"school": school, "branch": branch, "designation": "Teacher"})
        teacher_profile.staff = staff_record
        teacher_profile.school = school
        teacher_profile.branch = branch
        teacher_profile.save()

        math_sub, _ = Subject.objects.get_or_create(school=school, code="MATH", defaults={"name": "Mathematics"})
        sci_sub, _ = Subject.objects.get_or_create(school=school, code="SCI", defaults={"name": "Science"})

        ClassTeacherAssignment.objects.get_or_create(
            school=school,
            session=session,
            course=course10,
            section=sec_a,
            defaults={"staff": staff_record, "is_active": True},
        )
        SubjectTeacherAssignment.objects.get_or_create(
            school=school,
            session=session,
            course=course10,
            section=sec_a,
            subject=math_sub,
            defaults={"staff": staff_record, "is_active": True},
        )
        SubjectTeacherAssignment.objects.get_or_create(
            school=school,
            session=session,
            course=course10,
            section=sec_a,
            subject=sci_sub,
            defaults={"staff": staff_record, "is_active": True},
        )

        student_records = []
        for idx, data in enumerate(
            [
                ("ADM1001", "Riya", "Verma", course10, sec_a),
                ("ADM1002", "Kabir", "Singh", course10, sec_a),
                ("ADM1003", "Meera", "Khan", course9, sec_b),
                ("ADM1004", "Arjun", "Patel", course9, sec_b),
                ("ADM1005", "Anaya", "Das", course10, sec_a),
            ]
        ):
            admission_no, first, last, course, section = data
            obj, _ = Student.objects.get_or_create(
                school=school,
                admission_no=admission_no,
                defaults={
                    "first_name": first,
                    "last_name": last,
                    "course": course,
                    "section": section,
                    "guardian_name": f"Guardian {idx + 1}",
                    "guardian_phone": f"98999{idx + 100:05d}"[:10],
                    "is_active": True,
                },
            )
            student_records.append(obj)

        student_profile, _ = UserProfile.objects.get_or_create(user=student_user, defaults={"school": school, "branch": branch, "designation": "Student"})
        if student_records:
            student_profile.student = student_records[0]
        student_profile.school = school
        student_profile.branch = branch
        student_profile.save()

        today = date.today()
        for st in student_records:
            StudentAttendance.objects.get_or_create(
                school=school,
                student=st,
                attendance_date=today,
                defaults={"course": st.course, "section": st.section, "status": "P"},
            )

        StaffAttendance.objects.get_or_create(
            school=school,
            staff=staff_record,
            attendance_date=today,
            defaults={"status": "P"},
        )

        leave_type, _ = LeaveType.objects.get_or_create(school=school, name="Sick Leave", defaults={"max_days": 10})
        LeaveRequest.objects.get_or_create(
            school=school,
            leave_type=leave_type,
            staff=staff_record,
            from_date=today + timedelta(days=2),
            to_date=today + timedelta(days=3),
            defaults={"reason": "Sample leave request", "status": "pending"},
        )

        FeeHead.objects.get_or_create(school=school, name="Tuition Fee")
        for idx, st in enumerate(student_records[:3], start=1):
            FeeInvoice.objects.get_or_create(
                school=school,
                invoice_no=f"INV2026{idx:03d}",
                student=st,
                defaults={
                    "issue_date": today,
                    "due_date": today + timedelta(days=20),
                    "total_amount": Decimal("18500.00"),
                    "status": "issued",
                },
            )

        exp_cat, _ = ExpenseCategory.objects.get_or_create(school=school, name="Maintenance")
        ExpenseEntry.objects.get_or_create(
            school=school,
            category=exp_cat,
            expense_date=today,
            defaults={"amount": Decimal("5200.00"), "pay_mode": "cash", "notes": "Sample expense"},
        )

        self.stdout.write(self.style.SUCCESS("Sample seed complete for admin, teacher, and student portals."))
