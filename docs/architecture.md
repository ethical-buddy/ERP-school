# Architecture

## Design Goals

- Multi-school capable.
- Secure by default.
- Fast enough for day-to-day operations with thousands of records.
- Easy to add/remove features per school.

## Structure

- Project config in `config/`.
- Core tenancy and feature controls in `core/`.
- Domain modules separated per ERP area.
- Shared authentication and profile handling in `accounts/`.

## Security

- CSRF protection enabled.
- Strict password validation with minimum 12 characters.
- Argon2 password hasher preferred.
- Security headers middleware with CSP and permissions policy.
- Session and CSRF secure cookie flags via environment.

## Multi-School Scalability

- School-scoped base model inherited by operational entities.
- Branch and session entities isolate school context.
- Feature flags allow per-school module enablement.

## Performance

- Indexes on core query paths such as attendance date, class, and entity identifiers.
- Efficient list queries with `select_related` for high-use pages.
- Ready for DB connection pooling via persistent connections.
