from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .auth_views import TokenObtainPairThrottledView, TokenRefreshThrottledView

from .views import (
    AcademicSessionViewSet,
    AppointmentViewSet,
    AuthorViewSet,
    BookIssueViewSet,
    BookViewSet,
    CertificateTemplateViewSet,
    ComplaintViewSet,
    CourseViewSet,
    DepartmentViewSet,
    DesignationViewSet,
    EmailTemplateViewSet,
    EnquiryViewSet,
    ExamTermViewSet,
    ExamTypeViewSet,
    ExamViewSet,
    ExpenseCategoryViewSet,
    ExpenseEntryViewSet,
    FeatureFlagViewSet,
    FeeHeadViewSet,
    FeeInvoiceViewSet,
    FeePaymentViewSet,
    FeeStructureViewSet,
    FinancialYearViewSet,
    GatePassViewSet,
    GenreViewSet,
    HolidayViewSet,
    IDCardTemplateViewSet,
    ItemCategoryViewSet,
    ItemViewSet,
    LeaveRequestViewSet,
    LeaveTypeViewSet,
    LibraryViewSet,
    MarkRecordViewSet,
    MessageLogViewSet,
    NotificationTemplateViewSet,
    ProspectusLeadViewSet,
    RouteStopViewSet,
    RouteViewSet,
    SaleInvoiceViewSet,
    SaleLineViewSet,
    SchoolBranchViewSet,
    SchoolFeatureViewSet,
    SchoolViewSet,
    SectionViewSet,
    ServiceRequestViewSet,
    SmsTemplateViewSet,
    StaffAttendanceViewSet,
    StaffViewSet,
    StockEntryViewSet,
    StudentAttendanceViewSet,
    StudentCertificateViewSet,
    StudentDocumentTypeViewSet,
    StudentDocumentViewSet,
    StudentViewSet,
    SubjectViewSet,
    SupplierViewSet,
    TimetableSlotViewSet,
    TransportAssignmentViewSet,
    UserViewSet,
    VehicleTypeViewSet,
    VehicleViewSet,
    VisitorViewSet,
    health,
    me,
    readiness,
)

router = DefaultRouter()
router.register("users", UserViewSet, basename="api-users")

router.register("core/schools", SchoolViewSet, basename="api-schools")
router.register("core/branches", SchoolBranchViewSet, basename="api-branches")
router.register("core/academic-sessions", AcademicSessionViewSet, basename="api-academic-sessions")
router.register("core/financial-years", FinancialYearViewSet, basename="api-financial-years")
router.register("core/features", FeatureFlagViewSet, basename="api-features")
router.register("core/school-features", SchoolFeatureViewSet, basename="api-school-features")

router.register("academics/courses", CourseViewSet, basename="api-courses")
router.register("academics/sections", SectionViewSet, basename="api-sections")
router.register("academics/subjects", SubjectViewSet, basename="api-subjects")
router.register("academics/timetable-slots", TimetableSlotViewSet, basename="api-timetable-slots")

router.register("students", StudentViewSet, basename="api-students")
router.register("students/prospectus", ProspectusLeadViewSet, basename="api-prospectus")
router.register("students/document-types", StudentDocumentTypeViewSet, basename="api-student-document-types")
router.register("students/documents", StudentDocumentViewSet, basename="api-student-documents")
router.register("students/id-card-templates", IDCardTemplateViewSet, basename="api-id-card-templates")
router.register("students/certificate-templates", CertificateTemplateViewSet, basename="api-certificate-templates")
router.register("students/certificates", StudentCertificateViewSet, basename="api-student-certificates")

router.register("staff/departments", DepartmentViewSet, basename="api-departments")
router.register("staff/designations", DesignationViewSet, basename="api-designations")
router.register("staff", StaffViewSet, basename="api-staff")

router.register("attendance/holidays", HolidayViewSet, basename="api-holidays")
router.register("attendance/leave-types", LeaveTypeViewSet, basename="api-leave-types")
router.register("attendance/leave-requests", LeaveRequestViewSet, basename="api-leave-requests")
router.register("attendance/students", StudentAttendanceViewSet, basename="api-student-attendance")
router.register("attendance/staff", StaffAttendanceViewSet, basename="api-staff-attendance")

router.register("finance/fee-heads", FeeHeadViewSet, basename="api-fee-heads")
router.register("finance/fee-structures", FeeStructureViewSet, basename="api-fee-structures")
router.register("finance/invoices", FeeInvoiceViewSet, basename="api-fee-invoices")
router.register("finance/payments", FeePaymentViewSet, basename="api-fee-payments")
router.register("finance/expense-categories", ExpenseCategoryViewSet, basename="api-expense-categories")
router.register("finance/expenses", ExpenseEntryViewSet, basename="api-expenses")

router.register("transport/vehicle-types", VehicleTypeViewSet, basename="api-vehicle-types")
router.register("transport/vehicles", VehicleViewSet, basename="api-vehicles")
router.register("transport/routes", RouteViewSet, basename="api-routes")
router.register("transport/route-stops", RouteStopViewSet, basename="api-route-stops")
router.register("transport/assignments", TransportAssignmentViewSet, basename="api-transport-assignments")

router.register("library/libraries", LibraryViewSet, basename="api-libraries")
router.register("library/authors", AuthorViewSet, basename="api-authors")
router.register("library/genres", GenreViewSet, basename="api-genres")
router.register("library/books", BookViewSet, basename="api-books")
router.register("library/issues", BookIssueViewSet, basename="api-book-issues")

router.register("exams/types", ExamTypeViewSet, basename="api-exam-types")
router.register("exams/terms", ExamTermViewSet, basename="api-exam-terms")
router.register("exams/exams", ExamViewSet, basename="api-exams")
router.register("exams/marks", MarkRecordViewSet, basename="api-marks")

router.register("inventory/categories", ItemCategoryViewSet, basename="api-item-categories")
router.register("inventory/suppliers", SupplierViewSet, basename="api-suppliers")
router.register("inventory/items", ItemViewSet, basename="api-items")
router.register("inventory/stocks", StockEntryViewSet, basename="api-stocks")
router.register("inventory/sale-invoices", SaleInvoiceViewSet, basename="api-sale-invoices")
router.register("inventory/sale-lines", SaleLineViewSet, basename="api-sale-lines")

router.register("communication/sms-templates", SmsTemplateViewSet, basename="api-sms-templates")
router.register("communication/email-templates", EmailTemplateViewSet, basename="api-email-templates")
router.register("communication/notification-templates", NotificationTemplateViewSet, basename="api-notification-templates")
router.register("communication/message-logs", MessageLogViewSet, basename="api-message-logs")

router.register("frontoffice/visitors", VisitorViewSet, basename="api-visitors")
router.register("frontoffice/enquiries", EnquiryViewSet, basename="api-enquiries")
router.register("frontoffice/complaints", ComplaintViewSet, basename="api-complaints")
router.register("frontoffice/appointments", AppointmentViewSet, basename="api-appointments")
router.register("frontoffice/gate-passes", GatePassViewSet, basename="api-gate-passes")
router.register("frontoffice/service-requests", ServiceRequestViewSet, basename="api-service-requests")

urlpatterns = [
    path("v1/health/", health, name="api-health"),
    path("v1/readiness/", readiness, name="api-readiness"),
    path("v1/me/", me, name="api-me"),
    path("v1/auth/token/", TokenObtainPairThrottledView.as_view(), name="token_obtain_pair"),
    path("v1/auth/token/refresh/", TokenRefreshThrottledView.as_view(), name="token_refresh"),
    path("v1/", include(router.urls)),
]
