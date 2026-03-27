from django.urls import path

from . import views

app_name = "attendance"

urlpatterns = [
    path("", views.student_attendance_list, name="list"),
    path("create/", views.student_attendance_create, name="create"),
]
