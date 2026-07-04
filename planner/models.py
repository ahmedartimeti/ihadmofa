from datetime import time

from django.conf import settings
from django.db import models
from django.utils import timezone


class Task(models.Model):
    class Type(models.TextChoices):
        REVIEW = 'REVIEW', 'مطالعة'
        INCOMING = 'INCOMING', 'كتاب وارد'
        OUTGOING = 'OUTGOING', 'كتاب صادر'
        CIRCULAR = 'CIRCULAR', 'إعمام'
        DELIBERATION = 'DELIBERATION', 'مداولة'
        FOLLOWUP = 'FOLLOWUP', 'متابعة'
        MEETING = 'MEETING', 'اجتماع'
        CALL = 'CALL', 'اتصال'
        OTHER = 'OTHER', 'أخرى'

    class Priority(models.TextChoices):
        NORMAL = 'NORMAL', 'عادي'
        IMPORTANT = 'IMPORTANT', 'مهم'
        URGENT = 'URGENT', 'عاجل'

    class Status(models.TextChoices):
        OPEN = 'OPEN', 'مفتوح'
        DONE = 'DONE', 'منجز'
        DEFERRED = 'DEFERRED', 'مؤجل'
        OVERDUE = 'OVERDUE', 'متأخر'
        CANCELLED = 'CANCELLED', 'ملغاة'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=220)
    task_type = models.CharField(max_length=24, choices=Type.choices, default=Type.OTHER)
    reference_number = models.CharField(max_length=80, blank=True)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.NORMAL)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    due_date = models.DateField(default=timezone.localdate)
    due_time = models.TimeField(default=time(9, 0))
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['due_date', 'due_time', '-created_at']

    def __str__(self):
        return self.title
