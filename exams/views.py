import csv
import io
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from core.roles import can_manage_attendance
from students.models import Student

from .forms import ExamBulkUploadForm
from .models import Exam, ExamComponent, MarkRecord, StudentExamComponentMark


def _school_from_user(request):
    profile = getattr(request.user, "profile", None)
    if profile:
        return profile.school
    return None


@login_required
def exam_dashboard(request):
    if not can_manage_attendance(request.user):
        return HttpResponseForbidden("Exam module access denied")
    school = _school_from_user(request)
    exams = Exam.objects.select_related("course", "section", "subject").filter(school=school).order_by("-id") if school else Exam.objects.none()
    return render(request, "exams/dashboard.html", {"exams": exams})


@login_required
def exam_bulk_upload(request):
    if not can_manage_attendance(request.user):
        return HttpResponseForbidden("Exam module access denied")

    school = _school_from_user(request)
    form = ExamBulkUploadForm(request.POST or None, request.FILES or None, school=school)
    if request.method == "POST" and form.is_valid():
        exam = form.cleaned_data["exam"]
        csv_file = form.cleaned_data["marks_file"]
        if not csv_file.name.endswith(".csv"):
            messages.error(request, "Please upload a CSV file.")
            return redirect("exams:bulk_upload")

        components = {c.component_type: c for c in ExamComponent.objects.filter(school=exam.school, exam=exam)}
        decoded = csv_file.read().decode("utf-8")
        rows = csv.DictReader(io.StringIO(decoded))

        updated = 0
        for row in rows:
            admission_no = (row.get("admission_no") or "").strip()
            if not admission_no:
                continue
            student = Student.objects.filter(
                school=exam.school,
                admission_no=admission_no,
                course=exam.course,
                section=exam.section,
            ).first()
            if not student:
                continue

            values = {}
            total = Decimal("0")
            for key in ["theory", "internal", "practical"]:
                if key in components and row.get(key) not in (None, ""):
                    mark = Decimal(str(row.get(key)).strip())
                    if mark < 0 or mark > components[key].max_marks:
                        continue
                    values[key] = mark
                    total += mark

            if total > exam.max_marks:
                total = exam.max_marks

            record, _ = MarkRecord.objects.update_or_create(
                school=exam.school,
                exam=exam,
                student=student,
                defaults={"marks_obtained": total, "remarks": (row.get("remarks") or "")[:255]},
            )

            for key, mark in values.items():
                StudentExamComponentMark.objects.update_or_create(
                    school=exam.school,
                    record=record,
                    component=components[key],
                    defaults={"marks_obtained": mark, "uploaded_by": request.user},
                )
            updated += 1

        messages.success(request, f"Marks upload processed for {updated} students.")
        return redirect("exams:dashboard")

    return render(request, "exams/bulk_upload.html", {"form": form})
