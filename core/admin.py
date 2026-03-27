from django.contrib import admin

from .models import AcademicSession, AuditLog, FeatureFlag, FinancialYear, School, SchoolBranch, SchoolFeature

admin.site.register(School)
admin.site.register(SchoolBranch)
admin.site.register(AcademicSession)
admin.site.register(FinancialYear)
admin.site.register(FeatureFlag)
admin.site.register(SchoolFeature)
admin.site.register(AuditLog)
