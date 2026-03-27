from django.contrib import admin

from .models import ClassTeacherAssignment, Course, Section, Subject, SubjectTeacherAssignment, TimetableSlot

admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Subject)
admin.site.register(TimetableSlot)
admin.site.register(ClassTeacherAssignment)
admin.site.register(SubjectTeacherAssignment)
