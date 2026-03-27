#!/usr/bin/env bash
set -euo pipefail

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp -n .env.example .env || true
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
