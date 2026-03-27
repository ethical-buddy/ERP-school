# DB and Test Runbook (Arch Linux)

## Option A: Quick Local (SQLite)

```bash
cd erp_school_django
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Option B: PostgreSQL Local Service

```bash
sudo pacman -S postgresql
sudo -u postgres initdb -D /var/lib/postgres/data
sudo systemctl enable --now postgresql
sudo -u postgres psql
```

Inside `psql`:

```sql
CREATE USER erp_school WITH PASSWORD 'erp_school';
CREATE DATABASE erp_school OWNER erp_school;
\q
```

Edit `.env`:

```env
DB_ENGINE=postgres
POSTGRES_DB=erp_school
POSTGRES_USER=erp_school
POSTGRES_PASSWORD=erp_school
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
```

Run app:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Health Checks

```bash
python manage.py check --deploy
python manage.py test
```

## Smoke Test

1. Login at `http://127.0.0.1:8000/`.
2. Open dashboard.
3. Create School, Course, Section, Student, Staff from admin.
4. Create attendance and fee invoice from module screens.
