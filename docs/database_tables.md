# Database Tables (Current Django ERP)

This file lists the tables currently used in the new ERP and the feature area they serve.

## Core
- `core_school`: school master
- `core_schoolbranch`: school branch master
- `core_academicsession`: active academic sessions
- `core_financialyear`: financial years
- `core_featureflag`: feature registry
- `core_schoolfeature`: school-wise feature toggles
- `core_auditlog`: immutable audit trail of API write actions

## Accounts
- `accounts_userprofile`: links user to school/branch and mapped student/staff profile

## Academics
- `academics_course`: classes (Play/Nursery/LKG/UKG/1..12)
- `academics_section`: sections under classes
- `academics_subject`: subject master
- `academics_timetableslot`: timetable periods
- `academics_classteacherassignment`: class-teacher mapping
- `academics_subjectteacherassignment`: subject-teacher mapping per class-section

## Students
- `students_student`: student master
- `students_prospectuslead`: enquiry/prospectus pipeline
- `students_studentdocumenttype`: required student document types
- `students_studentdocument`: uploaded student documents
- `students_idcardtemplate`: ID card template
- `students_certificatetemplate`: certificate template
- `students_studentcertificate`: generated student certificates

## Staff
- `staff_department`: departments
- `staff_designation`: designations
- `staff_staff`: staff master
- `staff_staffdocumenttype`: staff document type

## Attendance
- `attendance_holiday`: holiday calendar
- `attendance_leavetype`: leave type master
- `attendance_leaverequest`: leave workflow
- `attendance_studentattendance`: daily student attendance
- `attendance_staffattendance`: daily staff attendance

## Finance
- `finance_feehead`: fee heads
- `finance_feestructure`: class-wise fee setup
- `finance_feeinvoice`: invoice records
- `finance_feepayment`: fee payments
- `finance_expensecategory`: expense category master
- `finance_expenseentry`: office expense entries

## Transport
- `transport_vehicletype`: vehicle type
- `transport_vehicle`: vehicle records
- `transport_route`: route master
- `transport_routestop`: route stops and fare
- `transport_transportassignment`: student-route assignments

## Library
- `librarymgmt_library`: library entities
- `librarymgmt_author`: author master
- `librarymgmt_genre`: genre master
- `librarymgmt_book`: book inventory
- `librarymgmt_bookissue`: issue/return records

## Exams
- `exams_examtype`: exam type
- `exams_examterm`: exam term
- `exams_exam`: exam definition
- `exams_examcomponent`: exam split (theory/internal/practical)
- `exams_markrecord`: total marks per student per exam
- `exams_studentexamcomponentmark`: component-level marks upload records

## Inventory
- `inventory_itemcategory`: item categories
- `inventory_supplier`: suppliers
- `inventory_item`: inventory items
- `inventory_stockentry`: stock in/out
- `inventory_saleinvoice`: sale invoices
- `inventory_saleline`: sale invoice lines

## Communication
- `communication_smstemplate`: SMS templates
- `communication_emailtemplate`: email templates
- `communication_notificationtemplate`: push templates
- `communication_messagelog`: outbound log

## Front Office
- `frontoffice_visitor`: visitor register
- `frontoffice_enquiry`: enquiries
- `frontoffice_complaint`: complaints
- `frontoffice_appointment`: appointments
- `frontoffice_gatepass`: gate pass entries
- `frontoffice_servicerequest`: service request entries

## Django Framework Tables
- `auth_*`, `django_admin_log`, `django_content_type`, `django_migrations`, `django_session`
