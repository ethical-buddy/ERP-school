from django.urls import path

from . import views

app_name = "students"

urlpatterns = [
    path("", views.student_list, name="list"),
    path("create/", views.student_create, name="create"),
]
