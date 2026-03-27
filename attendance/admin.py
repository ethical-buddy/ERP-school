from django.contrib import admin

from .models import Holiday, LeaveRequest, LeaveType, StaffAttendance, StudentAttendance

admin.site.register(Holiday)
admin.site.register(LeaveType)
admin.site.register(StudentAttendance)
admin.site.register(StaffAttendance)
admin.site.register(LeaveRequest)
