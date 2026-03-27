from django.db import models

from academics.models import Course
from core.models import SchoolScopedModel
from students.models import Student


class FeeHead(SchoolScopedModel):
    name = models.CharField(max_length=120)


class FeeStructure(SchoolScopedModel):
    fee_head = models.ForeignKey(FeeHead, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)


class FeeInvoice(SchoolScopedModel):
    invoice_no = models.CharField(max_length=50)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    issue_date = models.DateField()
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, default="draft")

    class Meta:
        unique_together = ("school", "invoice_no")


class FeePayment(SchoolScopedModel):
    invoice = models.ForeignKey(FeeInvoice, on_delete=models.CASCADE, related_name="payments")
    paid_on = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_mode = models.CharField(max_length=30, default="cash")
    reference_no = models.CharField(max_length=80, blank=True)


class ExpenseCategory(SchoolScopedModel):
    name = models.CharField(max_length=120)


class ExpenseEntry(SchoolScopedModel):
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    expense_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    pay_mode = models.CharField(max_length=30)
    notes = models.TextField(blank=True)
