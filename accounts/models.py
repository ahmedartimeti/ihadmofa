from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        DIRECTOR = 'DIRECTOR', 'Director'
        SECTION_HEAD = 'SECTION_HEAD', 'Section Head'
        EMPLOYEE = 'EMPLOYEE', 'Employee'
        VIEWER = 'VIEWER', 'Viewer'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.EMPLOYEE)
    full_name = models.CharField(max_length=150)
    department = models.CharField(max_length=150)
    section = models.CharField(max_length=150, blank=True)
    job_title = models.CharField(max_length=150, blank=True)
    email_for_alerts = models.EmailField(blank=True)
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    first_school = models.CharField(max_length=150, blank=True)
    birth_city = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name or self.user.username
