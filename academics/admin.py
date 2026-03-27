from django.contrib import admin

from .models import Course, Section, Subject, TimetableSlot

admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Subject)
admin.site.register(TimetableSlot)
