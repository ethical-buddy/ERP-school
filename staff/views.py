from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from core.roles import can_manage_staff
from .forms import StaffForm
from .models import Staff


@login_required
def staff_list(request):
    if not can_manage_staff(request.user):
        return HttpResponseForbidden("Staff module access denied")
    staff = Staff.objects.select_related("department", "designation").order_by("-id")[:200]
    return render(request, "staff/list.html", {"staff": staff})


@login_required
def staff_create(request):
    if not can_manage_staff(request.user):
        return HttpResponseForbidden("Staff module access denied")
    form = StaffForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("staff:list")
    return render(request, "staff/create.html", {"form": form})
