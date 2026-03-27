from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from core import views as core_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", auth_views.LoginView.as_view(template_name="auth/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", core_views.dashboard, name="dashboard"),
    path("module/<str:module_name>/", core_views.module_index, name="module_index"),
    path("students/", include("students.urls")),
    path("staff/", include("staff.urls")),
    path("attendance/", include("attendance.urls")),
    path("finance/", include("finance.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
