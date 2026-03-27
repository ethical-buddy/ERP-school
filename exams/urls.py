from django.urls import path

from . import views

app_name = "exams"

urlpatterns = [
    path("", views.exam_dashboard, name="dashboard"),
    path("bulk-upload/", views.exam_bulk_upload, name="bulk_upload"),
]
