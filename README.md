# IHAD

**Iraqi Integrated Hub for Administrative Diplomacy**  
**Official Workflow Management Platform**  
**Ministry of Foreign Affairs - Republic of Iraq**  
**Version 2.2**

IHAD is a Django workflow management platform for daily administrative tasks, follow-ups, reminders, reports, and employee planning.

## Production Release Scope

This release prepares the project for deployment on Render. It does not add new business features.

Prepared items:

- IHAD identity and login screen.
- Production Django settings.
- WhiteNoise static file serving.
- Static and media configuration.
- Render deployment files.
- SQLite retained for this phase.

## Local Setup

~~~bat
cd C:\Users\Admin-\Documents\Codex\2026-06-28\new-chat\mofa_smart_planner
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
~~~

Open:

~~~text
http://127.0.0.1:8000/
~~~

## Environment Variables

Create a .env file locally based on .env.example:

~~~env
SECRET_KEY=change-this-secret-key
DEBUG=False
ALLOWED_HOSTS=ihadmofa.onrender.com,127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=https://ihadmofa.onrender.com
SQLITE_PATH=/var/data/db.sqlite3
MEDIA_ROOT=/var/data/media
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
~~~

For local development you may use:

~~~env
DEBUG=True
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
~~~

## Static Files

~~~bat
python manage.py collectstatic --noinput
~~~

Static files are served using WhiteNoise.

## Media Files

Media files are configured through MEDIA_ROOT=/var/data/media.
On Render this is stored on the persistent disk defined in render.yaml.

## Deploying to GitHub

1. Create a GitHub repository.
2. From the project folder, run:

~~~bat
git init
git add .
git commit -m "IHAD production release 2.2"
git branch -M main
git remote add origin https://github.com/YOUR-USER/YOUR-REPOSITORY.git
git push -u origin main
~~~

## Deploying to Render

Target service name: ihadmofa

Expected URL: https://ihadmofa.onrender.com

If the name is unavailable, choose the closest available name, such as ihad-mofa, ihad-mofa-platform, or ihad-workflow.

## Render Web Service Steps

1. Open Render Dashboard.
2. Click New +.
3. Choose Web Service.
4. Connect your GitHub repository.
5. Select the IHAD repository.
6. Use these settings:

~~~text
Environment: Python
Build Command: pip install -r requirements.txt && python manage.py collectstatic --noinput
Start Command: gunicorn mofa_smart_planner.wsgi:application --log-file -
~~~

Or use the included render.yaml blueprint.

## Render Environment Variables

~~~text
SECRET_KEY=(generate a secure value)
DEBUG=False
ALLOWED_HOSTS=ihadmofa.onrender.com
CSRF_TRUSTED_ORIGINS=https://ihadmofa.onrender.com
SQLITE_PATH=/var/data/db.sqlite3
MEDIA_ROOT=/var/data/media
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
~~~

Optional Web Push variables, only when activating device notifications:

~~~text
WEBPUSH_VAPID_PUBLIC_KEY=
WEBPUSH_VAPID_PRIVATE_KEY=
WEBPUSH_VAPID_ADMIN_EMAIL=
~~~

## Persistent SQLite on Render

This phase keeps SQLite as requested. SQLite is suitable for pilot/testing only. For official long-term production, PostgreSQL is recommended later. The project includes a persistent disk in render.yaml:

~~~text
mountPath: /var/data
SQLITE_PATH=/var/data/db.sqlite3
MEDIA_ROOT=/var/data/media
~~~

Do not remove the disk if you want database and uploaded media persistence. Render persistent disks may require a paid plan; without a disk, SQLite data can be lost after redeploys.

## Running Migrations on Render

After the first deploy, open Render Shell and run:

~~~bash
python manage.py migrate
~~~

## Creating Superuser on Render

~~~bash
python manage.py createsuperuser
~~~

## Collecting Static Files on Render

~~~bash
python manage.py collectstatic --noinput
~~~

## Health Check Commands

~~~bat
python manage.py check
python manage.py migrate
python manage.py collectstatic --noinput
~~~

## Files for Deployment

- Procfile
- runtime.txt
- render.yaml
- .env.example
- requirements.txt
- mofa_smart_planner/settings.py

## Notes

- This release keeps SQLite and does not move to PostgreSQL.
- Email, Firebase, Flutter, AI, and new reports are not part of this release.
- Device notifications require HTTPS and VAPID keys when enabled.
