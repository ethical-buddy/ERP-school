from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import FeeInvoiceForm
from .models import FeeInvoice


@login_required
def invoice_list(request):
    invoices = FeeInvoice.objects.select_related("student").order_by("-id")[:200]
    return render(request, "finance/list.html", {"invoices": invoices})


@login_required
def invoice_create(request):
    form = FeeInvoiceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("finance:list")
    return render(request, "finance/create.html", {"form": form})
