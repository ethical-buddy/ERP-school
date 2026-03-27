from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from core.roles import can_manage_finance
from .forms import FeeInvoiceForm
from .models import FeeInvoice


@login_required
def invoice_list(request):
    if not can_manage_finance(request.user):
        return HttpResponseForbidden("Finance module access denied")
    invoices = FeeInvoice.objects.select_related("student").order_by("-id")[:200]
    return render(request, "finance/list.html", {"invoices": invoices})


@login_required
def invoice_create(request):
    if not can_manage_finance(request.user):
        return HttpResponseForbidden("Finance module access denied")
    form = FeeInvoiceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("finance:list")
    return render(request, "finance/create.html", {"form": form})
