# API v1 Reference

Base path: `/api/v1/`
Auth: JWT Bearer token

## Auth

- `POST /api/v1/auth/token/`
  - payload: `{"username":"...","password":"..."}`
  - returns: `access`, `refresh`
- `POST /api/v1/auth/token/refresh/`
  - payload: `{"refresh":"..."}`
  - returns: new `access`

## Utility

- `GET /api/v1/health/`
- `GET /api/v1/me/`

## Users

- `GET /api/v1/users/`
- `POST /api/v1/users/`

## Core ERP Endpoints

- `GET|POST|PUT|PATCH|DELETE /api/v1/students/`
- `GET|POST|PUT|PATCH|DELETE /api/v1/staff/`
- `GET|POST|PUT|PATCH|DELETE /api/v1/attendance/students/`
- `GET|POST|PUT|PATCH|DELETE /api/v1/finance/invoices/`

## Filtering and Search

- `?search=<text>` for configured search fields.
- `?ordering=<field>` e.g. `ordering=-created_at`.
- `?limit=50&offset=0` pagination.

## School Scope

- Non-superuser access is constrained to `UserProfile.school`.
- Superusers can query all data, and can narrow with `?school_id=<id>`.

## Role Rules

- Read operations: any authenticated user.
- Write operations: superuser or users in groups `api_admin` or `api_manager`.

## Throttling

- Authenticated: 300 requests/minute.
- Anonymous: 50 requests/minute.
