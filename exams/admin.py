from django.contrib import admin

from .models import Exam, ExamTerm, ExamType, MarkRecord

admin.site.register(ExamType)
admin.site.register(ExamTerm)
admin.site.register(Exam)
admin.site.register(MarkRecord)
