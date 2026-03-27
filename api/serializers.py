from django.contrib.auth.models import Group, User
from rest_framework import serializers

from academics.models import Course, Section, Subject, TimetableSlot
from attendance.models import Holiday, LeaveRequest, LeaveType, StaffAttendance, StudentAttendance
from communication.models import EmailTemplate, MessageLog, NotificationTemplate, SmsTemplate
from core.models import AcademicSession, FeatureFlag, FinancialYear, School, SchoolBranch, SchoolFeature
from exams.models import Exam, ExamTerm, ExamType, MarkRecord
from finance.models import ExpenseCategory, ExpenseEntry, FeeHead, FeeInvoice, FeePayment, FeeStructure
from frontoffice.models import Appointment, Complaint, Enquiry, GatePass, ServiceRequest, Visitor
from inventory.models import Item, ItemCategory, SaleInvoice, SaleLine, StockEntry, Supplier
from librarymgmt.models import Author, Book, BookIssue, Genre, Library
from staff.models import Department, Designation, Staff
from students.models import CertificateTemplate, IDCardTemplate, ProspectusLead, Student, StudentCertificate, StudentDocument, StudentDocumentType
from transport.models import Route, RouteStop, TransportAssignment, Vehicle, VehicleType


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


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = "__all__"


class SchoolBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolBranch
        fields = "__all__"


class AcademicSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        fields = "__all__"


class FinancialYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialYear
        fields = "__all__"


class FeatureFlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureFlag
        fields = "__all__"


class SchoolFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolFeature
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class TimetableSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimetableSlot
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class ProspectusLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProspectusLead
        fields = "__all__"


class StudentDocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDocumentType
        fields = "__all__"


class StudentDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDocument
        fields = "__all__"


class IDCardTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = IDCardTemplate
        fields = "__all__"


class CertificateTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificateTemplate
        fields = "__all__"


class StudentCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCertificate
        fields = "__all__"


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = "__all__"


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = "__all__"


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = "__all__"


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = "__all__"


class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = "__all__"


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAttendance
        fields = "__all__"


class StaffAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffAttendance
        fields = "__all__"


class FeeHeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeHead
        fields = "__all__"


class FeeStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeStructure
        fields = "__all__"


class FeeInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeInvoice
        fields = "__all__"


class FeePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeePayment
        fields = "__all__"


class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = "__all__"


class ExpenseEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseEntry
        fields = "__all__"


class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = "__all__"


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = "__all__"


class RouteStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteStop
        fields = "__all__"


class TransportAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportAssignment
        fields = "__all__"


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = "__all__"


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class BookIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookIssue
        fields = "__all__"


class ExamTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamType
        fields = "__all__"


class ExamTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamTerm
        fields = "__all__"


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = "__all__"


class MarkRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkRecord
        fields = "__all__"


class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields = "__all__"


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class StockEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = StockEntry
        fields = "__all__"


class SaleInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleInvoice
        fields = "__all__"


class SaleLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleLine
        fields = "__all__"


class SmsTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmsTemplate
        fields = "__all__"


class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = "__all__"


class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = "__all__"


class MessageLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageLog
        fields = "__all__"


class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = "__all__"


class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = "__all__"


class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = "__all__"


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"


class GatePassSerializer(serializers.ModelSerializer):
    class Meta:
        model = GatePass
        fields = "__all__"


class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = "__all__"
