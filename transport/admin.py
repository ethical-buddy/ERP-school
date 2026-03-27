from django.contrib import admin

from .models import Route, RouteStop, TransportAssignment, Vehicle, VehicleType

admin.site.register(VehicleType)
admin.site.register(Vehicle)
admin.site.register(Route)
admin.site.register(RouteStop)
admin.site.register(TransportAssignment)
