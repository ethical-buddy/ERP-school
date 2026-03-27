from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from attendance.models import LeaveRequest, StaffAttendance, StudentAttendance
from finance.models import ExpenseEntry, FeeInvoice
from staff.models import Staff
from students.models import Student


def _in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


def _role_context(user):
    return {
        "is_admin_portal": user.is_superuser or _in_group(user, "admin_portal"),
        "is_teacher_portal": _in_group(user, "teacher_portal"),
        "is_student_portal": _in_group(user, "student_portal"),
    }


@login_required
def post_login_router(request):
    role = _role_context(request.user)
    if role["is_admin_portal"]:
        return redirect("admin_portal")
    if role["is_teacher_portal"]:
        return redirect("teacher_portal")
    if role["is_student_portal"]:
        return redirect("student_portal")
    return redirect("dashboard")


@login_required
def dashboard(request):
    context = {
        "student_count": Student.objects.count(),
        "staff_count": Staff.objects.count(),
        "invoice_count": FeeInvoice.objects.count(),
        "expense_count": ExpenseEntry.objects.count(),
        "student_attendance_count": StudentAttendance.objects.count(),
        "staff_attendance_count": StaffAttendance.objects.count(),
        "students_by_class": list(Student.objects.values("course__name").annotate(total=Count("id")).order_by("course__name")[:8]),
    }
    context.update(_role_context(request.user))
    return render(request, "dashboard.html", context)


@login_required
def admin_portal(request):
    role = _role_context(request.user)
    if not role["is_admin_portal"]:
        return HttpResponseForbidden("Admin portal access denied")

    context = {
        "student_count": Student.objects.count(),
        "staff_count": Staff.objects.count(),
        "invoice_count": FeeInvoice.objects.count(),
        "expense_count": ExpenseEntry.objects.count(),
        "pending_leave_count": LeaveRequest.objects.filter(status="pending").count(),
        "recent_invoices": FeeInvoice.objects.select_related("student").order_by("-id")[:8],
    }
    context.update(role)
    return render(request, "portals/admin.html", context)


@login_required
def teacher_portal(request):
    role = _role_context(request.user)
    if not role["is_teacher_portal"] and not role["is_admin_portal"]:
        return HttpResponseForbidden("Teacher portal access denied")

    context = {
        "student_count": Student.objects.count(),
        "today_attendance": StudentAttendance.objects.order_by("-attendance_date")[:25],
        "today_staff_attendance": StaffAttendance.objects.order_by("-attendance_date")[:25],
        "open_leaves": LeaveRequest.objects.filter(status="pending").order_by("-id")[:10],
    }
    context.update(role)
    return render(request, "portals/teacher.html", context)


@login_required
def student_portal(request):
    role = _role_context(request.user)
    if not role["is_student_portal"] and not role["is_admin_portal"]:
        return HttpResponseForbidden("Student portal access denied")

    recent_students = Student.objects.select_related("course", "section").order_by("-id")[:10]
    context = {
        "recent_students": recent_students,
        "attendance_records": StudentAttendance.objects.select_related("student").order_by("-attendance_date")[:20],
        "invoices": FeeInvoice.objects.select_related("student").order_by("-issue_date")[:10],
    }
    context.update(role)
    return render(request, "portals/student.html", context)


@login_required
def module_index(request, module_name):
    mapping = {
        "academics": "Academic Structure, Subjects, Timetable, Class Mapping",
        "students": "Admission, Prospectus, ID Cards, Certificates, Document Tracking",
        "staff": "Employee Master, Departments, Designation, Staff Profiles",
        "attendance": "Student Attendance, Staff Attendance, Leave Types, Holidays, Leave Workflow",
        "finance": "Fee Heads, Fee Structure, Invoicing, Collections, Office Expenses",
        "transport": "Vehicles, Routes, Stops, Student Transport Assignments",
        "library": "Library Master, Books, Authors, Genres, Issue and Return",
        "exams": "Exam Types, Terms, Exam Schedule, Marks Entry, Report Cards",
        "inventory": "Item Categories, Suppliers, Stock, Sales, Student Balance",
        "communication": "SMS/Email/Push Templates, Message Logs, Notification Management",
        "frontoffice": "Visitor, Enquiry, Complaints, Appointments, Gate Pass, Service Requests",
    }
    context = {
        "module_name": module_name,
        "module_description": mapping.get(module_name, "Module"),
    }
    context.update(_role_context(request.user))
    return render(request, "module.html", context)
