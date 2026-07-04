from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from notifications.models import Notification, PushSubscription
from notifications.views import _send_web_push
from planner.models import Task


class Command(BaseCommand):
    help = 'Send web push notifications for tasks due within the next five minutes.'

    def handle(self, *args, **options):
        now = timezone.localtime()
        today = now.date()
        current_minutes = now.hour * 60 + now.minute
        window_end = current_minutes + 5
        sent_count = 0

        tasks = Task.objects.filter(
            due_date=today,
            status__in=[Task.Status.OPEN, Task.Status.DEFERRED],
        ).select_related('user')

        for task in tasks:
            task_minutes = task.due_time.hour * 60 + task.due_time.minute
            if task_minutes < current_minutes or task_minutes > window_end:
                continue

            notification_key = f'تنبيه مهمة #{task.pk}'
            if Notification.objects.filter(user=task.user, title=notification_key, scheduled_at__date=today).exists():
                continue

            subscriptions = PushSubscription.objects.filter(user=task.user, is_active=True)
            if not subscriptions.exists():
                continue

            message = f'اقترب موعد: {task.title} - الساعة {task.due_time.strftime("%H:%M")}'
            any_sent = False
            for subscription in subscriptions:
                ok, _message = _send_web_push(subscription, 'تنبيه مهمة', message)
                any_sent = any_sent or ok

            Notification.objects.create(
                user=task.user,
                title=notification_key,
                message=message,
                scheduled_at=timezone.now(),
                status=Notification.Status.SENT if any_sent else Notification.Status.PENDING,
            )
            if any_sent:
                sent_count += 1

        self.stdout.write(self.style.SUCCESS(f'Sent push notifications for {sent_count} task(s).'))
