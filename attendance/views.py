from datetime import date

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from academics.models import ClassTeacherAssignment
from accounts.models import UserProfile
from core.roles import can_manage_attendance, is_admin
from students.models import Student

from .forms import StudentAttendanceForm
from .models import StudentAttendance


def _teacher_scope(request):
    if is_admin(request.user):
        return ClassTeacherAssignment.objects.select_related("course", "section", "staff").filter(is_active=True)
    profile = UserProfile.objects.filter(user=request.user).select_related("staff").first()
    if not profile or not profile.staff_id:
        return ClassTeacherAssignment.objects.none()
    return ClassTeacherAssignment.objects.select_related("course", "section", "staff").filter(staff_id=profile.staff_id, is_active=True)


@login_required
def student_attendance_list(request):
    if not can_manage_attendance(request.user):
        return HttpResponseForbidden("Attendance module access denied")
    records = StudentAttendance.objects.select_related("student").order_by("-attendance_date")[:200]
    return render(request, "attendance/list.html", {"records": records})


@login_required
def student_attendance_create(request):
    if not can_manage_attendance(request.user):
        return HttpResponseForbidden("Attendance module access denied")
    form = StudentAttendanceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("attendance:list")
    return render(request, "attendance/create.html", {"form": form})


@login_required
def class_teacher_attendance(request):
    if not can_manage_attendance(request.user):
        return HttpResponseForbidden("Attendance module access denied")

    assignments = _teacher_scope(request)
    selected_assignment = None
    selected_date = request.POST.get("attendance_date") or request.GET.get("attendance_date") or str(date.today())
    assignment_id = request.POST.get("assignment_id") or request.GET.get("assignment_id")

    if assignment_id:
        selected_assignment = assignments.filter(id=assignment_id).first()

    students = []
    existing_map = {}
    if selected_assignment:
        students = list(
            Student.objects.filter(
                school=selected_assignment.school,
                course=selected_assignment.course,
                section=selected_assignment.section,
                is_active=True,
            )
            .order_by("first_name", "last_name")
            .values("id", "admission_no", "first_name", "last_name")
        )
        for rec in StudentAttendance.objects.filter(
            school=selected_assignment.school,
            course=selected_assignment.course,
            section=selected_assignment.section,
            attendance_date=selected_date,
            student_id__in=[s["id"] for s in students],
        ):
            existing_map[rec.student_id] = rec.status

    if request.method == "POST" and selected_assignment:
        for s in students:
            status = request.POST.get(f"status_{s['id']}")
            if status not in {"P", "A", "L"}:
                continue
            StudentAttendance.objects.update_or_create(
                school=selected_assignment.school,
                student_id=s["id"],
                attendance_date=selected_date,
                defaults={
                    "course": selected_assignment.course,
                    "section": selected_assignment.section,
                    "status": status,
                },
            )
            existing_map[s["id"]] = status
        return redirect(f"/attendance/class-teacher/?assignment_id={selected_assignment.id}&attendance_date={selected_date}")

    context = {
        "assignments": assignments,
        "selected_assignment": selected_assignment,
        "selected_date": selected_date,
        "students": students,
        "existing_map": existing_map,
    }
    return render(request, "attendance/class_teacher_mark.html", context)
