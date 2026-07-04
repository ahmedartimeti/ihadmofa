#!/bin/sh
set -e
python manage.py migrate --noinput
exec gunicorn mofa_smart_planner.wsgi:application --bind 0.0.0.0:${PORT:-8000} --log-file -
