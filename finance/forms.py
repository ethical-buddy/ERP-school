from django import forms

from .models import FeeInvoice


class FeeInvoiceForm(forms.ModelForm):
    class Meta:
        model = FeeInvoice
        fields = ["school", "invoice_no", "student", "issue_date", "due_date", "total_amount", "status"]
