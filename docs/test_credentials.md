# Test Credentials

Seed command:

```bash
cd erp_school_django
. .venv/bin/activate
python manage.py seed_sample_data
```

## Web Login Accounts

- Admin portal user
  - Username: `admin_demo`
  - Password: `Admin@12345678`
  - Portal URL: `http://127.0.0.1:8000/portal/admin/`

- Teacher portal user
  - Username: `teacher_demo`
  - Password: `Teacher@12345678`
  - Portal URL: `http://127.0.0.1:8000/portal/teacher/`

- Student portal user
  - Username: `student_demo`
  - Password: `Student@12345678`
  - Portal URL: `http://127.0.0.1:8000/portal/student/`

- Legacy superuser from initial seed
  - Username: `admin`
  - Password: `Admin@12345678`

## API JWT Example

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin_demo","password":"Admin@12345678"}'
```

Use `access` token in header:

```bash
Authorization: Bearer <access-token>
```
