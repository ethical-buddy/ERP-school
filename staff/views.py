from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import StaffForm
from .models import Staff


@login_required
def staff_list(request):
    staff = Staff.objects.select_related("department", "designation").order_by("-id")[:200]
    return render(request, "staff/list.html", {"staff": staff})


@login_required
def staff_create(request):
    form = StaffForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("staff:list")
    return render(request, "staff/create.html", {"form": form})
