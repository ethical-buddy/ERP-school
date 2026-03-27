from django.db import models

from core.models import SchoolScopedModel
from students.models import Student


class ItemCategory(SchoolScopedModel):
    name = models.CharField(max_length=120)


class Supplier(SchoolScopedModel):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20, blank=True)


class Item(SchoolScopedModel):
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=120)
    sku = models.CharField(max_length=50)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        unique_together = ("school", "sku")


class StockEntry(SchoolScopedModel):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    entry_type = models.CharField(max_length=10, choices=(("IN", "IN"), ("OUT", "OUT")))
    entry_date = models.DateField()


class SaleInvoice(SchoolScopedModel):
    invoice_no = models.CharField(max_length=50)
    student = models.ForeignKey(Student, null=True, blank=True, on_delete=models.SET_NULL)
    invoice_date = models.DateField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        unique_together = ("school", "invoice_no")


class SaleLine(SchoolScopedModel):
    invoice = models.ForeignKey(SaleInvoice, on_delete=models.CASCADE, related_name="lines")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)
