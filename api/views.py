from django.contrib.auth.models import User
from django.db import connection
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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

from .permissions import IsAdminManagerOrReadOnly
from .audit import AuditLogMixin
from .school_scope import SchoolScopedQuerysetMixin
from .serializers import (
    AcademicSessionSerializer,
    AppointmentSerializer,
    AttendanceSerializer,
    AuthorSerializer,
    BookIssueSerializer,
    BookSerializer,
    CertificateTemplateSerializer,
    ComplaintSerializer,
    CourseSerializer,
    DepartmentSerializer,
    DesignationSerializer,
    EmailTemplateSerializer,
    EnquirySerializer,
    ExamSerializer,
    ExamTermSerializer,
    ExamTypeSerializer,
    ExpenseCategorySerializer,
    ExpenseEntrySerializer,
    FeatureFlagSerializer,
    FeeHeadSerializer,
    FeeInvoiceSerializer,
    FeePaymentSerializer,
    FeeStructureSerializer,
    FinancialYearSerializer,
    GatePassSerializer,
    GenreSerializer,
    HolidaySerializer,
    IDCardTemplateSerializer,
    ItemCategorySerializer,
    ItemSerializer,
    LeaveRequestSerializer,
    LeaveTypeSerializer,
    LibrarySerializer,
    MarkRecordSerializer,
    MessageLogSerializer,
    NotificationTemplateSerializer,
    ProspectusLeadSerializer,
    RouteSerializer,
    RouteStopSerializer,
    SaleInvoiceSerializer,
    SaleLineSerializer,
    SchoolBranchSerializer,
    SchoolFeatureSerializer,
    SchoolSerializer,
    SectionSerializer,
    ServiceRequestSerializer,
    SmsTemplateSerializer,
    StaffAttendanceSerializer,
    StaffSerializer,
    StockEntrySerializer,
    StudentCertificateSerializer,
    StudentDocumentSerializer,
    StudentDocumentTypeSerializer,
    StudentSerializer,
    SubjectSerializer,
    SupplierSerializer,
    TimetableSlotSerializer,
    TransportAssignmentSerializer,
    UserCreateSerializer,
    UserSerializer,
    VehicleSerializer,
    VehicleTypeSerializer,
    VisitorSerializer,
)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def health(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        db_ok = cursor.fetchone()[0] == 1
    return Response({"status": "ok", "user": request.user.username, "database": "ok" if db_ok else "error"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def readiness(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        db_ok = cursor.fetchone()[0] == 1
    return Response({"ready": db_ok})


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


class ReadWriteViewSet(AuditLogMixin, SchoolScopedQuerysetMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminManagerOrReadOnly]
    search_fields = ["id"]
    ordering_fields = ["id", "created_at", "updated_at"]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        school_id = self.get_user_school()
        if school_id is None and request.user.is_superuser:
            school_id = data.get("school")
        if school_id is None:
            raise PermissionDenied("School context is required for this user.")
        data.setdefault("school", school_id)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        school_id = self.get_user_school()
        if school_id is None and self.request.user.is_superuser:
            school_id = self.request.data.get("school")
        if school_id is None:
            raise PermissionDenied("School context is required for this user.")
        instance = serializer.save(school_id=school_id)
        self._write_audit("create", instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        self._write_audit("update", instance)

    def perform_destroy(self, instance):
        self._write_audit("delete", instance)
        instance.delete()


class SchoolViewSet(AuditLogMixin, viewsets.ModelViewSet):
    queryset = School.objects.order_by("-id")
    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticated, IsAdminManagerOrReadOnly]
    search_fields = ["name", "code", "email"]
    ordering_fields = ["id", "name", "code", "created_at"]


class SchoolBranchViewSet(ReadWriteViewSet):
    queryset = SchoolBranch.objects.order_by("-id")
    serializer_class = SchoolBranchSerializer
    search_fields = ["name", "code", "address"]


class AcademicSessionViewSet(ReadWriteViewSet):
    queryset = AcademicSession.objects.order_by("-id")
    serializer_class = AcademicSessionSerializer
    search_fields = ["title"]


class FinancialYearViewSet(ReadWriteViewSet):
    queryset = FinancialYear.objects.order_by("-id")
    serializer_class = FinancialYearSerializer
    search_fields = ["title"]


class FeatureFlagViewSet(viewsets.ModelViewSet):
    queryset = FeatureFlag.objects.order_by("-id")
    serializer_class = FeatureFlagSerializer
    permission_classes = [IsAuthenticated, IsAdminManagerOrReadOnly]
    search_fields = ["slug", "name"]


class SchoolFeatureViewSet(ReadWriteViewSet):
    queryset = SchoolFeature.objects.select_related("feature").order_by("-id")
    serializer_class = SchoolFeatureSerializer
    search_fields = ["feature__slug", "feature__name"]


class CourseViewSet(ReadWriteViewSet):
    queryset = Course.objects.order_by("-id")
    serializer_class = CourseSerializer
    search_fields = ["name", "code"]


class SectionViewSet(ReadWriteViewSet):
    queryset = Section.objects.select_related("course").order_by("-id")
    serializer_class = SectionSerializer
    search_fields = ["name", "course__name"]


class SubjectViewSet(ReadWriteViewSet):
    queryset = Subject.objects.order_by("-id")
    serializer_class = SubjectSerializer
    search_fields = ["name", "code"]


class TimetableSlotViewSet(ReadWriteViewSet):
    queryset = TimetableSlot.objects.select_related("course", "section", "subject").order_by("-id")
    serializer_class = TimetableSlotSerializer


class StudentViewSet(ReadWriteViewSet):
    queryset = Student.objects.select_related("course", "section").order_by("-id")
    serializer_class = StudentSerializer
    filterset_fields = ["course", "section", "gender", "is_active"]
    search_fields = ["admission_no", "first_name", "last_name", "guardian_name"]


class ProspectusLeadViewSet(ReadWriteViewSet):
    queryset = ProspectusLead.objects.order_by("-id")
    serializer_class = ProspectusLeadSerializer
    search_fields = ["enquiry_no", "student_name", "contact_phone", "status"]


class StudentDocumentTypeViewSet(ReadWriteViewSet):
    queryset = StudentDocumentType.objects.order_by("-id")
    serializer_class = StudentDocumentTypeSerializer
    search_fields = ["name"]


class StudentDocumentViewSet(ReadWriteViewSet):
    queryset = StudentDocument.objects.select_related("student", "document_type").order_by("-id")
    serializer_class = StudentDocumentSerializer


class IDCardTemplateViewSet(ReadWriteViewSet):
    queryset = IDCardTemplate.objects.order_by("-id")
    serializer_class = IDCardTemplateSerializer
    search_fields = ["name"]


class CertificateTemplateViewSet(ReadWriteViewSet):
    queryset = CertificateTemplate.objects.order_by("-id")
    serializer_class = CertificateTemplateSerializer
    search_fields = ["name"]


class StudentCertificateViewSet(ReadWriteViewSet):
    queryset = StudentCertificate.objects.select_related("student", "template").order_by("-id")
    serializer_class = StudentCertificateSerializer
    search_fields = ["certificate_no", "student__admission_no", "student__first_name"]


class DepartmentViewSet(ReadWriteViewSet):
    queryset = Department.objects.order_by("-id")
    serializer_class = DepartmentSerializer
    search_fields = ["name"]


class DesignationViewSet(ReadWriteViewSet):
    queryset = Designation.objects.order_by("-id")
    serializer_class = DesignationSerializer
    search_fields = ["name"]


class StaffViewSet(ReadWriteViewSet):
    queryset = Staff.objects.select_related("department", "designation").order_by("-id")
    serializer_class = StaffSerializer
    filterset_fields = ["department", "designation", "is_active"]
    search_fields = ["employee_id", "first_name", "last_name", "phone", "email"]


class HolidayViewSet(ReadWriteViewSet):
    queryset = Holiday.objects.order_by("-date", "-id")
    serializer_class = HolidaySerializer
    filterset_fields = ["date"]
    search_fields = ["title"]


class LeaveTypeViewSet(ReadWriteViewSet):
    queryset = LeaveType.objects.order_by("-id")
    serializer_class = LeaveTypeSerializer
    search_fields = ["name"]


class LeaveRequestViewSet(ReadWriteViewSet):
    queryset = LeaveRequest.objects.select_related("student", "staff", "leave_type").order_by("-id")
    serializer_class = LeaveRequestSerializer
    filterset_fields = ["leave_type", "student", "staff", "status"]


class StudentAttendanceViewSet(ReadWriteViewSet):
    queryset = StudentAttendance.objects.select_related("student", "course", "section").order_by("-attendance_date", "-id")
    serializer_class = AttendanceSerializer
    filterset_fields = ["course", "section", "student", "status", "attendance_date"]
    search_fields = ["student__admission_no", "student__first_name", "student__last_name"]


class StaffAttendanceViewSet(ReadWriteViewSet):
    queryset = StaffAttendance.objects.select_related("staff").order_by("-attendance_date", "-id")
    serializer_class = StaffAttendanceSerializer
    filterset_fields = ["staff", "status", "attendance_date"]


class FeeHeadViewSet(ReadWriteViewSet):
    queryset = FeeHead.objects.order_by("-id")
    serializer_class = FeeHeadSerializer
    search_fields = ["name"]


class FeeStructureViewSet(ReadWriteViewSet):
    queryset = FeeStructure.objects.select_related("fee_head", "course").order_by("-id")
    serializer_class = FeeStructureSerializer
    filterset_fields = ["fee_head", "course"]


class FeeInvoiceViewSet(ReadWriteViewSet):
    queryset = FeeInvoice.objects.select_related("student").order_by("-issue_date", "-id")
    serializer_class = FeeInvoiceSerializer
    filterset_fields = ["student", "status", "issue_date", "due_date"]
    search_fields = ["invoice_no", "student__admission_no", "student__first_name", "student__last_name"]


class FeePaymentViewSet(ReadWriteViewSet):
    queryset = FeePayment.objects.select_related("invoice").order_by("-paid_on", "-id")
    serializer_class = FeePaymentSerializer
    filterset_fields = ["invoice", "payment_mode", "paid_on"]


class ExpenseCategoryViewSet(ReadWriteViewSet):
    queryset = ExpenseCategory.objects.order_by("-id")
    serializer_class = ExpenseCategorySerializer
    search_fields = ["name"]


class ExpenseEntryViewSet(ReadWriteViewSet):
    queryset = ExpenseEntry.objects.select_related("category").order_by("-expense_date", "-id")
    serializer_class = ExpenseEntrySerializer
    filterset_fields = ["category", "expense_date", "pay_mode"]


class VehicleTypeViewSet(ReadWriteViewSet):
    queryset = VehicleType.objects.order_by("-id")
    serializer_class = VehicleTypeSerializer
    search_fields = ["name"]


class VehicleViewSet(ReadWriteViewSet):
    queryset = Vehicle.objects.select_related("vehicle_type").order_by("-id")
    serializer_class = VehicleSerializer
    search_fields = ["registration_no", "driver_name"]


class RouteViewSet(ReadWriteViewSet):
    queryset = Route.objects.order_by("-id")
    serializer_class = RouteSerializer
    search_fields = ["name", "code"]


class RouteStopViewSet(ReadWriteViewSet):
    queryset = RouteStop.objects.select_related("route").order_by("-id")
    serializer_class = RouteStopSerializer
    search_fields = ["name", "route__name", "route__code"]


class TransportAssignmentViewSet(ReadWriteViewSet):
    queryset = TransportAssignment.objects.select_related("student", "route", "stop").order_by("-id")
    serializer_class = TransportAssignmentSerializer
    filterset_fields = ["student", "route", "stop"]


class LibraryViewSet(ReadWriteViewSet):
    queryset = Library.objects.order_by("-id")
    serializer_class = LibrarySerializer
    search_fields = ["name"]


class AuthorViewSet(ReadWriteViewSet):
    queryset = Author.objects.order_by("-id")
    serializer_class = AuthorSerializer
    search_fields = ["name"]


class GenreViewSet(ReadWriteViewSet):
    queryset = Genre.objects.order_by("-id")
    serializer_class = GenreSerializer
    search_fields = ["name"]


class BookViewSet(ReadWriteViewSet):
    queryset = Book.objects.select_related("library", "author", "genre").order_by("-id")
    serializer_class = BookSerializer
    search_fields = ["title", "isbn"]


class BookIssueViewSet(ReadWriteViewSet):
    queryset = BookIssue.objects.select_related("student", "book").order_by("-id")
    serializer_class = BookIssueSerializer
    filterset_fields = ["student", "book", "issue_date", "return_date"]


class ExamTypeViewSet(ReadWriteViewSet):
    queryset = ExamType.objects.order_by("-id")
    serializer_class = ExamTypeSerializer
    search_fields = ["name"]


class ExamTermViewSet(ReadWriteViewSet):
    queryset = ExamTerm.objects.order_by("-id")
    serializer_class = ExamTermSerializer
    search_fields = ["name"]


class ExamViewSet(ReadWriteViewSet):
    queryset = Exam.objects.select_related("exam_type", "exam_term", "course", "section", "subject").order_by("-id")
    serializer_class = ExamSerializer
    filterset_fields = ["exam_type", "exam_term", "course", "section", "subject", "exam_date"]


class MarkRecordViewSet(ReadWriteViewSet):
    queryset = MarkRecord.objects.select_related("exam", "student").order_by("-id")
    serializer_class = MarkRecordSerializer
    filterset_fields = ["exam", "student"]


class ItemCategoryViewSet(ReadWriteViewSet):
    queryset = ItemCategory.objects.order_by("-id")
    serializer_class = ItemCategorySerializer
    search_fields = ["name"]


class SupplierViewSet(ReadWriteViewSet):
    queryset = Supplier.objects.order_by("-id")
    serializer_class = SupplierSerializer
    search_fields = ["name", "phone"]


class ItemViewSet(ReadWriteViewSet):
    queryset = Item.objects.select_related("category", "supplier").order_by("-id")
    serializer_class = ItemSerializer
    filterset_fields = ["category", "supplier"]
    search_fields = ["name", "sku"]


class StockEntryViewSet(ReadWriteViewSet):
    queryset = StockEntry.objects.select_related("item").order_by("-entry_date", "-id")
    serializer_class = StockEntrySerializer
    filterset_fields = ["item", "entry_type", "entry_date"]


class SaleInvoiceViewSet(ReadWriteViewSet):
    queryset = SaleInvoice.objects.select_related("student").order_by("-invoice_date", "-id")
    serializer_class = SaleInvoiceSerializer
    filterset_fields = ["student", "invoice_date"]
    search_fields = ["invoice_no"]


class SaleLineViewSet(ReadWriteViewSet):
    queryset = SaleLine.objects.select_related("invoice", "item").order_by("-id")
    serializer_class = SaleLineSerializer
    filterset_fields = ["invoice", "item"]


class SmsTemplateViewSet(ReadWriteViewSet):
    queryset = SmsTemplate.objects.order_by("-id")
    serializer_class = SmsTemplateSerializer
    search_fields = ["name"]


class EmailTemplateViewSet(ReadWriteViewSet):
    queryset = EmailTemplate.objects.order_by("-id")
    serializer_class = EmailTemplateSerializer
    search_fields = ["name", "subject"]


class NotificationTemplateViewSet(ReadWriteViewSet):
    queryset = NotificationTemplate.objects.order_by("-id")
    serializer_class = NotificationTemplateSerializer
    search_fields = ["name", "title"]


class MessageLogViewSet(ReadWriteViewSet):
    queryset = MessageLog.objects.order_by("-id")
    serializer_class = MessageLogSerializer
    filterset_fields = ["channel", "status"]
    search_fields = ["recipient"]


class VisitorViewSet(ReadWriteViewSet):
    queryset = Visitor.objects.order_by("-visit_date", "-id")
    serializer_class = VisitorSerializer
    search_fields = ["name", "phone", "purpose"]


class EnquiryViewSet(ReadWriteViewSet):
    queryset = Enquiry.objects.order_by("-id")
    serializer_class = EnquirySerializer
    filterset_fields = ["status"]
    search_fields = ["name", "phone", "query"]


class ComplaintViewSet(ReadWriteViewSet):
    queryset = Complaint.objects.order_by("-id")
    serializer_class = ComplaintSerializer
    filterset_fields = ["status", "complaint_type"]
    search_fields = ["raised_by", "detail"]


class AppointmentViewSet(ReadWriteViewSet):
    queryset = Appointment.objects.order_by("-appointment_date", "-id")
    serializer_class = AppointmentSerializer
    filterset_fields = ["status", "appointment_date"]
    search_fields = ["person_name", "appointment_for"]


class GatePassViewSet(ReadWriteViewSet):
    queryset = GatePass.objects.select_related("student").order_by("-issue_date", "-id")
    serializer_class = GatePassSerializer
    filterset_fields = ["student", "issue_date"]
    search_fields = ["issued_to", "reason"]


class ServiceRequestViewSet(ReadWriteViewSet):
    queryset = ServiceRequest.objects.order_by("-id")
    serializer_class = ServiceRequestSerializer
    filterset_fields = ["status"]
    search_fields = ["requester", "title", "detail"]
