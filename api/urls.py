from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import FeeInvoiceViewSet, StaffViewSet, StudentAttendanceViewSet, StudentViewSet, UserViewSet, health, me

router = DefaultRouter()
router.register("users", UserViewSet, basename="api-users")
router.register("students", StudentViewSet, basename="api-students")
router.register("staff", StaffViewSet, basename="api-staff")
router.register("attendance/students", StudentAttendanceViewSet, basename="api-student-attendance")
router.register("finance/invoices", FeeInvoiceViewSet, basename="api-fee-invoices")

urlpatterns = [
    path("v1/health/", health, name="api-health"),
    path("v1/me/", me, name="api-me"),
    path("v1/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("v1/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("v1/", include(router.urls)),
]
