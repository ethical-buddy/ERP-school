from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from core.roles import can_manage_students
from .forms import StudentForm
from .models import Student


@login_required
def student_list(request):
    if not can_manage_students(request.user):
        return HttpResponseForbidden("Students module access denied")
    students = Student.objects.select_related("course", "section").order_by("-id")[:200]
    return render(request, "students/list.html", {"students": students})


@login_required
def student_create(request):
    if not can_manage_students(request.user):
        return HttpResponseForbidden("Students module access denied")
    form = StudentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("students:list")
    return render(request, "students/create.html", {"form": form})
