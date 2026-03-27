from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import StudentForm
from .models import Student


@login_required
def student_list(request):
    students = Student.objects.select_related("course", "section").order_by("-id")[:200]
    return render(request, "students/list.html", {"students": students})


@login_required
def student_create(request):
    form = StudentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("students:list")
    return render(request, "students/create.html", {"form": form})
