from django.contrib import admin

from .models import Appointment, Complaint, Enquiry, GatePass, ServiceRequest, Visitor

admin.site.register(Visitor)
admin.site.register(Enquiry)
admin.site.register(Complaint)
admin.site.register(Appointment)
admin.site.register(GatePass)
admin.site.register(ServiceRequest)
