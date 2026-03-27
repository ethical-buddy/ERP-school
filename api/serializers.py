from django.contrib.auth.models import Group, User
from rest_framework import serializers

from attendance.models import StudentAttendance
from finance.models import FeeInvoice
from staff.models import Staff
from students.models import Student


class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "is_active", "roles"]

    def get_roles(self, obj):
        return list(obj.groups.values_list("name", flat=True))


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=12)
    roles = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "is_active", "roles"]

    def create(self, validated_data):
        roles = validated_data.pop("roles", [])
        user = User.objects.create_user(**validated_data)
        if roles:
            groups = Group.objects.filter(name__in=roles)
            user.groups.set(groups)
        return user


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "id",
            "school",
            "admission_no",
            "first_name",
            "last_name",
            "dob",
            "gender",
            "course",
            "section",
            "guardian_name",
            "guardian_phone",
            "address",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = [
            "id",
            "school",
            "employee_id",
            "first_name",
            "last_name",
            "department",
            "designation",
            "phone",
            "email",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAttendance
        fields = [
            "id",
            "school",
            "student",
            "course",
            "section",
            "attendance_date",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class FeeInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeInvoice
        fields = [
            "id",
            "school",
            "invoice_no",
            "student",
            "issue_date",
            "due_date",
            "total_amount",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
