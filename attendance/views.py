from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import StudentAttendanceForm
from .models import StudentAttendance


@login_required
def student_attendance_list(request):
    records = StudentAttendance.objects.select_related("student").order_by("-attendance_date")[:200]
    return render(request, "attendance/list.html", {"records": records})


@login_required
def student_attendance_create(request):
    form = StudentAttendanceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("attendance:list")
    return render(request, "attendance/create.html", {"form": form})
