from django.urls import path

from . import views

app_name = "finance"

urlpatterns = [
    path("", views.invoice_list, name="list"),
    path("create/", views.invoice_create, name="create"),
]
