from django.contrib import admin

from .models import ExpenseCategory, ExpenseEntry, FeeHead, FeeInvoice, FeePayment, FeeStructure

admin.site.register(FeeHead)
admin.site.register(FeeStructure)
admin.site.register(FeeInvoice)
admin.site.register(FeePayment)
admin.site.register(ExpenseCategory)
admin.site.register(ExpenseEntry)
