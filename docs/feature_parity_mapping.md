# Feature Parity Mapping: Legacy to New Django ERP

## Core and Multi-School

- Legacy school/branch/session/year setup mapped to: `core.School`, `core.SchoolBranch`, `core.AcademicSession`, `core.FinancialYear`.
- Feature enable/disable per school mapped to: `core.FeatureFlag`, `core.SchoolFeature`.

## Module-to-App Mapping

- Student Information + Admission + Certificates -> `students`.
- Staff + HR masters -> `staff`.
- Attendance + Leave + Holidays -> `attendance`.
- Finance + Expenses -> `finance`.
- Transport -> `transport`.
- Library -> `librarymgmt`.
- Marks and Exams -> `exams`.
- Inventory + sales -> `inventory`.
- Communication templates + logs -> `communication`.
- Front Office workflow -> `frontoffice`.
- Academics + timetable entities -> `academics`.

## UI and Operations

- Dashboard + module entry points available at `/dashboard/`.
- High-frequency operations currently exposed with direct pages:
  - Students
  - Staff
  - Student Attendance
  - Fee Invoices
- Full CRUD for all mapped entities available via Django Admin.

## What Is Deferred to API Phase

- REST API endpoints, token auth, mobile-specific controllers, and API rate-limits.
- See `docs/api_phase_plan.md`.
