from django.db import models

from core.models import SchoolScopedModel
from students.models import Student


class VehicleType(SchoolScopedModel):
    name = models.CharField(max_length=80)


class Vehicle(SchoolScopedModel):
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    registration_no = models.CharField(max_length=40)
    driver_name = models.CharField(max_length=120)
    capacity = models.PositiveIntegerField(default=0)


class Route(SchoolScopedModel):
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=40)

    class Meta:
        unique_together = ("school", "code")


class RouteStop(SchoolScopedModel):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="stops")
    name = models.CharField(max_length=120)
    fare = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class TransportAssignment(SchoolScopedModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    stop = models.ForeignKey(RouteStop, null=True, blank=True, on_delete=models.SET_NULL)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
