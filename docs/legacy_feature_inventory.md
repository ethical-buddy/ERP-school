# Legacy ERP Feature Inventory (Extracted from Existing Code)

Source baseline:
- `routes/web.php`
- `routes/api.php`
- `routes/inventorymanagement.php`
- `routes/transport_attendance_management.php`
- module controllers and migrations under `app/Http/Controllers/MasterAdmin`, `database/migrations`

## Setup and Auth

- School setup wizard: school, branch, academic session, financial year, admin creation.
- Login, OTP verification, resend OTP, forgot/reset password, two-factor status.
- User profile, password change, login history, logout.

## Dashboard and Global

- Main dashboard and homework summary.
- Academic year / financial year switch.
- Bookmarks links.
- Global search and quick lookup.
- Global print / export file / export PDF.

## Student Information / Admission

- Student registration and edit.
- Prospectus entry, edit, payment.
- Admission form print.
- Student import and bulk update.
- Student information field settings.
- Student reports: class-wise, inactive, credentials, prospectus, birthday.
- Student document types and document tracking.
- Student ID card generation and template master settings.
- Student account status update.
- Session transfer / promotions / sibling and profile updates.

## Certificates

- Certificate template and field integration.
- Generate certificates and transfer certificate.
- Certificate preview, PDF, edit, delete.
- Certificate reports.

## Transport

- Vehicle type, vehicle, route, route stop, travel agency.
- Route relation and route head assignment.
- Student transport assignment (individual and class-wise).
- Transport fee integration.
- Transport MIS reports (route/driver/class/defaulters).
- Mobile transport attendance and stop-wise assignment workflow.

## Attendance

- Student attendance (daily and bulk).
- Staff attendance.
- Leave types and leave workflow.
- Holidays.
- Attendance reports: day-wise, class-wise, student MIS, staff MIS.

## Timetable

- Timetable definitions and class timetable uploads.
- Subject mapping and period/lunch timing.
- Class-wise, teacher-wise timetable reports.
- Teacher workload and substitution management.

## Communication

- Communication types and sender settings.
- DLT entity config.
- Header/footer config.
- SMS copy settings.
- Mobile app notification config.
- Phonebook groups and contacts.
- SMS and email template management.
- Phonebook import/export.
- Compose/bulk/individual SMS sending.
- SMS reports and failure resend.
- Auto-send SMS events.

## In-App Content / App Module

- Homework.
- Notice.
- Assignment.
- Syllabus.
- Downloads.
- Circular and school news.
- Calendar and calendar type.
- Push notification device token storage.

## Library

- Library masters: library, category, racks, author, tags, genres.
- Book master and bulk book import.
- Issue/return book operations.
- Daily entry reports.

## Marks and Exam Management

- Default setting.
- Subject-wise and student-wise marks entry.
- Marks import and attendance import.
- Student exam result processing.
- Hall ticket and report card generation.
- Exam master settings: type, term, assessment, activities, grade system.
- Subject skill and skill group.
- Subject-course mapping and exam configuration.
- Other entry types and remarks.
- Total attendance class-wise.
- Online exam question categories and online exam APIs.

## Finance

- Fee head, fee account, installment, concession, fine setting.
- Fee collection, receipt settings, receipt modify/cancel records.
- Daily/periodic finance reports.
- Student fee reports.

## Payroll

- Leave and assigned leave setup.
- Staff salary definition.
- Month-wise working days.
- Late count setup.
- Staff attendance correction.
- Salary report, salary entry, paid salary report, salary slip print.

## Office Expenses

- Expense category, subcategory, pay mode.
- Expense entry.
- Quick balance and units.
- Daily finance book.
- Expense voucher and daily book reports.

## Inventory Management

- Item category, publisher, supplier masters.
- Item master and stock management.
- Stock history.
- Sale book set and sales history.
- Student inventory balance and invoice previews.

## Front Office

- Enquiry, visitor, appointment, complaint, service request.
- Gate pass.
- Purpose, reference, visiting type, status and observation masters.

## Global Settings and User Admin

- School metadata.
- Academic sessions and financial years.
- Currencies, languages, city, category, house, title, religion, blood group, gender.
- Role and user management.
- Certificate and barcode settings.

## Mobile App API Surface (Current Legacy)

- Student app: profile, attendance, timetable, fee report, notice, homework, assignment, syllabus, exam result, library, transport, calendar, certificates, downloads, leave, online exam/class.
- Teacher app: attendance entry, homework/assignment/notice/syllabus/news, marks entry, timetable, salary, leave, transport attendance, student updates.
- Receptionist app: home panel.
- Auth APIs: login, OTP, password reset, profile.
