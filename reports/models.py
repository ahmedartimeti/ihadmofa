from django.conf import settings
from django.db import models
from django.utils import timezone

class DailyReport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='daily_reports')
    report_date = models.DateField(default=timezone.localdate)
    completed_tasks = models.PositiveIntegerField(default=0)
    open_tasks = models.PositiveIntegerField(default=0)
    deferred_tasks = models.PositiveIntegerField(default=0)
    urgent_tasks = models.PositiveIntegerField(default=0)
    important_tasks = models.PositiveIntegerField(default=0)
    normal_tasks = models.PositiveIntegerField(default=0)
    summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'report_date')
        ordering = ['-report_date']

    def __str__(self):
        return f'{self.user} - {self.report_date}'
