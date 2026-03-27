from django.contrib import admin

from .models import Department, Designation, Staff, StaffDocumentType

admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Staff)
admin.site.register(StaffDocumentType)
