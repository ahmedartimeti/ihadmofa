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

Media files use the default local media folder. On Render Free, uploaded media and SQLite data are temporary and may be lost after redeploys or restarts.

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
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
~~~

Optional Web Push variables, only when activating device notifications:

~~~text
WEBPUSH_VAPID_PUBLIC_KEY=
WEBPUSH_VAPID_PRIVATE_KEY=
WEBPUSH_VAPID_ADMIN_EMAIL=
~~~

## SQLite on Render Free

This phase keeps SQLite as requested. The included render.yaml is compatible with Render Free and does not define a persistent disk. This is useful for first deployment testing only.

Warning: SQLite data and uploaded media on Render Free are not permanent. Data can be lost after redeploys, rebuilds, or restarts.

Later upgrade paths without major project changes:

- Upgrade to a Render plan that supports a persistent disk, then set SQLITE_PATH and MEDIA_ROOT to the disk mount path.
- Move to PostgreSQL for official long-term production.


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
