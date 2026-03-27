from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from core import views as core_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("", auth_views.LoginView.as_view(template_name="auth/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("post-login/", core_views.post_login_router, name="post_login"),
    path("dashboard/", core_views.dashboard, name="dashboard"),
    path("portal/admin/", core_views.admin_portal, name="admin_portal"),
    path("portal/teacher/", core_views.teacher_portal, name="teacher_portal"),
    path("portal/student/", core_views.student_portal, name="student_portal"),
    path("module/<str:module_name>/", core_views.module_index, name="module_index"),
    path("students/", include("students.urls")),
    path("staff/", include("staff.urls")),
    path("attendance/", include("attendance.urls")),
    path("finance/", include("finance.urls")),
    path("exams/", include("exams.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
