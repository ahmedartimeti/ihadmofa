import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from accounts.models import UserProfile


class Command(BaseCommand):
    help = 'Create or update the configured IHAD admin account.'

    def handle(self, *args, **options):
        username = os.environ.get('ADMIN_USERNAME', 'Adminahmed').strip()
        email = os.environ.get('ADMIN_EMAIL', '').strip()
        password = os.environ.get('ADMIN_PASSWORD', '').strip()
        reset_password = os.environ.get('ADMIN_RESET_PASSWORD', 'False') == 'True'

        if not password:
            self.stdout.write('ADMIN_PASSWORD is not set; skipping admin account setup.')
            return

        User = get_user_model()
        user, created = User.objects.get_or_create(username=username, defaults={'email': email})
        user.email = email or user.email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        if created or reset_password:
            user.set_password(password)
        user.save()

        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'full_name': os.environ.get('ADMIN_FULL_NAME', username),
                'department': os.environ.get('ADMIN_DEPARTMENT', 'Administration'),
            },
        )
        profile.role = UserProfile.Role.ADMIN
        if not profile.full_name:
            profile.full_name = os.environ.get('ADMIN_FULL_NAME', username)
        if not profile.department:
            profile.department = os.environ.get('ADMIN_DEPARTMENT', 'Administration')
        profile.email_for_alerts = email or profile.email_for_alerts
        profile.save()

        status = 'created' if created else 'updated'
        self.stdout.write(self.style.SUCCESS(f'Admin account {status}: {username}'))
