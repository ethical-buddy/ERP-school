from django.contrib import admin

from .models import Exam, ExamComponent, ExamTerm, ExamType, MarkRecord, StudentExamComponentMark

admin.site.register(ExamType)
admin.site.register(ExamTerm)
admin.site.register(Exam)
admin.site.register(ExamComponent)
admin.site.register(MarkRecord)
admin.site.register(StudentExamComponentMark)
