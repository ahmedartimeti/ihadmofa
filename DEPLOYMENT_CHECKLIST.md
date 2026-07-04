# IHAD Deployment Checklist

## Identity Check

- [x] System name appears as IHAD.
- [x] Full name appears as Iraqi Integrated Hub for Administrative Diplomacy.
- [x] Ministry of Foreign Affairs appears in login/footer/brand text.
- [x] Republic of Iraq appears in login/footer text.
- [x] Version 2.2 appears in footer/ribbon.

## Login Check

- [x] Login screen uses Django authentication form.
- [x] Login form posts to accounts:login.
- [x] CSRF token is present.
- [x] Registration form remains Django-based and separate from Sign In.

## Local Command Check

The local command output provided by the user confirms:

- [x] python -m pip install -r requirements.txt completed successfully.
- [x] python manage.py check completed successfully with no issues.
- [x] python manage.py migrate applies the pending planner migration when run as a separate command.

Commands to run before final upload:

~~~bat
python manage.py makemigrations
python manage.py migrate
python manage.py check
python manage.py collectstatic --noinput
python manage.py runserver
~~~

Note: This Codex environment blocked direct command execution, so command verification relies on the user's local CMD output plus static project inspection.

## Deployment Files Check

- [x] requirements.txt exists and includes Django, Pillow, pywebpush, whitenoise, gunicorn, python-dotenv.
- [x] Procfile exists.
- [x] runtime.txt exists.
- [x] README.md exists and contains Render instructions.
- [x] .gitignore exists and excludes .env and generated/cache files.
- [x] render.yaml exists.
- [x] .env.example exists.

## Production Settings Check

- [x] SECRET_KEY reads from Environment Variable.
- [x] DEBUG reads from Environment Variable.
- [x] ALLOWED_HOSTS includes localhost/127.0.0.1 and ihadmofa.onrender.com defaults.
- [x] CSRF_TRUSTED_ORIGINS includes https://ihadmofa.onrender.com.
- [x] WhiteNoise is enabled when installed.
- [x] STATIC_ROOT is configured.
- [x] STATICFILES_DIRS points to static.
- [x] MEDIA_ROOT is configurable through Environment Variable.
- [x] Media files are served in local mode and configured for Render disk.

## Render Instructions Check

- [x] Build Command documented:

~~~text
pip install -r requirements.txt && python manage.py collectstatic --noinput
~~~

- [x] Start Command documented:

~~~text
gunicorn mofa_smart_planner.wsgi:application --log-file -
~~~

- [x] Environment Variables documented.
- [x] Migrate command documented.
- [x] Superuser command documented.
- [x] Persistent disk warning documented for SQLite.

## Warnings

- SQLite remains enabled as requested. It is acceptable for pilot/testing only.
- On Render, SQLite must use a persistent disk mounted at /var/data. Without a persistent disk, database data can be lost after redeploys or service rebuilds.
- For official long-term production, migrate later to PostgreSQL.
- Device push notifications require HTTPS and VAPID keys. They are prepared but not required for the first deployment.
- No email, Flutter, Firebase, AI, or new report features were added in this final deployment check.

## Remaining Before Deployment

- [ ] Run python manage.py migrate one final time and confirm no unapplied migrations.
- [ ] Run python manage.py collectstatic --noinput before or during Render build.
- [ ] Create GitHub repository and push the project.
- [ ] Create Render service using render.yaml or the README settings.
- [ ] Add Render Environment Variables.
- [ ] Create superuser on Render after first migrate.

## Deployment Readiness Decision

Status: READY FOR RENDER PILOT DEPLOYMENT.

Condition: Use persistent disk for SQLite, or accept that SQLite without disk is only temporary/testing data.
