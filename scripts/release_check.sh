#!/usr/bin/env bash
set -euo pipefail

. .venv/bin/activate
python manage.py check
python manage.py test
python manage.py check --deploy
python manage.py collectstatic --noinput
