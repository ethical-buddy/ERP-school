# ERP School (Django)

Production-oriented, modular, secure school ERP web application built with Django.

## Highlights

- Multi-school architecture using school-scoped models.
- Modular apps for admissions, staff, attendance, finance, transport, library, exams, inventory, communication, front office.
- Security-first defaults with strict password validators, secure headers, CSRF/session hardening.
- Fast web operations with indexed models, scoped domain entities, and simple dashboard reporting.
- Web app only for now; API layer intentionally left for a later phase.

## Project Layout

- `config/`: Django project configuration and URL routing.
- `core/`: school tenancy core models, feature flags, security middleware, dashboard.
- `students/`, `staff/`, `attendance/`, `finance/`, `academics/`, `transport/`, `librarymgmt/`, `exams/`, `inventory/`, `communication/`, `frontoffice/`: ERP modules.
- `templates/`, `static/`: UI layer.
- `docs/`: architecture, feature parity, DB and test runbooks.

## Quick Start

1. Create and activate virtualenv.
2. Install requirements.
3. Copy `.env.example` to `.env` and edit values.
4. Run migrations.
5. Create superuser.
6. Run server.

See `docs/db_and_test_runbook.md` for exact commands.

## Feature Parity

Legacy features extracted from the existing codebase are listed in `docs/legacy_feature_inventory.md`.
Mapping to the new Django architecture is documented in `docs/feature_parity_mapping.md`.

## API Plan

Phase 2 API is now available with JWT auth at `/api/v1/`.
Reference: `docs/api_v1_reference.md`.
Further expansion is documented in `docs/phases.md` and `docs/api_phase_plan.md`.
