from django.contrib.auth.models import User
from rest_framework import mixins, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from attendance.models import StudentAttendance
from finance.models import FeeInvoice
from staff.models import Staff
from students.models import Student

from .permissions import IsAdminManagerOrReadOnly
from .school_scope import SchoolScopedQuerysetMixin
from .serializers import AttendanceSerializer, FeeInvoiceSerializer, StaffSerializer, StudentSerializer, UserCreateSerializer, UserSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def health(request):
    return Response({"status": "ok", "user": request.user.username})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    return Response(UserSerializer(request.user).data)


class UserViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.order_by("id")
    permission_classes = [IsAuthenticated, IsAdminManagerOrReadOnly]
    search_fields = ["username", "email"]

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer


class StudentViewSet(SchoolScopedQuerysetMixin, viewsets.ModelViewSet):
    queryset = Student.objects.select_related("course", "section").order_by("-id")
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsAdminManagerOrReadOnly]
    filterset_fields = ["course", "section", "gender", "is_active"]
    search_fields = ["admission_no", "first_name", "last_name", "guardian_name"]
    ordering_fields = ["id", "admission_no", "first_name", "created_at"]


class StaffViewSet(SchoolScopedQuerysetMixin, viewsets.ModelViewSet):
    queryset = Staff.objects.select_related("department", "designation").order_by("-id")
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated, IsAdminManagerOrReadOnly]
    filterset_fields = ["department", "designation", "is_active"]
    search_fields = ["employee_id", "first_name", "last_name", "phone", "email"]
    ordering_fields = ["id", "employee_id", "first_name", "created_at"]


class StudentAttendanceViewSet(SchoolScopedQuerysetMixin, viewsets.ModelViewSet):
    queryset = StudentAttendance.objects.select_related("student", "course", "section").order_by("-attendance_date", "-id")
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, IsAdminManagerOrReadOnly]
    filterset_fields = ["course", "section", "student", "status", "attendance_date"]
    search_fields = ["student__admission_no", "student__first_name", "student__last_name"]
    ordering_fields = ["id", "attendance_date", "created_at"]


class FeeInvoiceViewSet(SchoolScopedQuerysetMixin, viewsets.ModelViewSet):
    queryset = FeeInvoice.objects.select_related("student").order_by("-issue_date", "-id")
    serializer_class = FeeInvoiceSerializer
    permission_classes = [IsAuthenticated, IsAdminManagerOrReadOnly]
    filterset_fields = ["student", "status", "issue_date", "due_date"]
    search_fields = ["invoice_no", "student__admission_no", "student__first_name", "student__last_name"]
    ordering_fields = ["id", "invoice_no", "issue_date", "created_at"]
