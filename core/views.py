from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render

from attendance.models import StaffAttendance, StudentAttendance
from finance.models import ExpenseEntry, FeeInvoice
from staff.models import Staff
from students.models import Student


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
    return render(request, "dashboard.html", context)


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
    return render(request, "module.html", context)
