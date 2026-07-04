from datetime import time
from django.conf import settings
from django.db import models
from django.utils import timezone

class Meeting(models.Model):
    class Status(models.TextChoices):
        OPEN = 'OPEN', 'قادم'
        DONE = 'DONE', 'منجز'
        DEFERRED = 'DEFERRED', 'مؤجل'
        CANCELLED = 'CANCELLED', 'ملغى'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='meetings')
    title = models.CharField(max_length=220)
    meeting_date = models.DateField(default=timezone.localdate)
    meeting_time = models.TimeField(default=time(10, 0))
    location = models.CharField(max_length=180, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['meeting_date', 'meeting_time']

    def __str__(self):
        return self.title
