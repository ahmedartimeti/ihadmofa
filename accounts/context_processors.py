from datetime import timedelta

from django.urls import reverse
from django.utils import timezone


def profile_context(request):
    if not request.user.is_authenticated:
        return {'current_profile': None, 'quick_summary': None, 'startup_tasks': [], 'alert_items': []}

    from accounts.utils import restrict_queryset
    from planner.models import Task

    today = timezone.localdate()
    tomorrow = today + timedelta(days=1)
    tasks = restrict_queryset(Task.objects.all(), request.user)
    startup_tasks = tasks.filter(due_date=today).exclude(status=Task.Status.DONE).order_by('due_time', 'title')[:8]

    alert_items = []
    for task in tasks.filter(due_date=today).exclude(status=Task.Status.DONE):
        alert_items.append({
            'kind': 'task',
            'key': f'task-{task.pk}-{task.due_date}-{task.due_time}',
            'title': task.title,
            'date': task.due_date,
            'time': task.due_time,
            'meta': task.get_task_type_display(),
            'notes': task.notes or 'لا توجد ملاحظات إضافية.',
            'done_url': reverse('planner:task_done', args=[task.pk]),
            'defer_url': reverse('planner:task_defer', args=[task.pk]),
            'delete_url': reverse('planner:task_delete', args=[task.pk]),
        })

    return {
        'current_profile': getattr(request.user, 'profile', None),
        'current_date': today,
        'startup_tasks': startup_tasks,
        'alert_items': alert_items,
        'quick_summary': {
            'work_start': '07:00',
            'work_end': '14:00',
            'today_count': tasks.filter(due_date=today).count(),
            'tomorrow_count': tasks.filter(due_date=tomorrow).count(),
            'urgent_today': tasks.filter(due_date=today, priority=Task.Priority.URGENT).count(),
            'urgent_tomorrow': tasks.filter(due_date=tomorrow, priority=Task.Priority.URGENT).count(),
            'past_count': tasks.filter(due_date__lt=today).count(),
            'future_count': tasks.filter(due_date__gt=tomorrow).count(),
        }
    }
