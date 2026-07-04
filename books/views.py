from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils import timezone
from accounts.utils import restrict_queryset
from planner.models import Task

BOOKS_FOLLOWUP_TYPES = [
    Task.Type.REVIEW,
    Task.Type.INCOMING,
    Task.Type.OUTGOING,
    Task.Type.CIRCULAR,
    Task.Type.FOLLOWUP,
    Task.Type.DELIBERATION,
    Task.Type.MEETING,
    Task.Type.CALL,
    Task.Type.OTHER,
]


def _period_filter(qs, period):
    today = timezone.localdate()
    if period == 'today':
        return qs.filter(due_date=today)
    if period == 'week':
        start = today - timedelta(days=today.weekday())
        return qs.filter(due_date__gte=start, due_date__lte=start + timedelta(days=6))
    if period == 'month':
        return qs.filter(due_date__year=today.year, due_date__month=today.month)
    if period == 'year':
        return qs.filter(due_date__year=today.year)
    return qs


@login_required
def book_list(request):
    base_items = restrict_queryset(Task.objects.filter(task_type__in=BOOKS_FOLLOWUP_TYPES), request.user)
    items = base_items
    q = request.GET.get('q', '').strip()
    period = request.GET.get('period', 'all')
    sort = request.GET.get('sort', 'due_date')
    task_type = request.GET.get('type', '')
    status = request.GET.get('status', '')
    priority = request.GET.get('priority', '')

    if q:
        items = items.filter(Q(title__icontains=q) | Q(notes__icontains=q) | Q(reference_number__icontains=q))
    if task_type in BOOKS_FOLLOWUP_TYPES:
        items = items.filter(task_type=task_type)
    if status in [Task.Status.OPEN, Task.Status.DONE, Task.Status.DEFERRED, Task.Status.OVERDUE, Task.Status.CANCELLED]:
        items = items.filter(status=status)
    if priority in [Task.Priority.URGENT, Task.Priority.IMPORTANT, Task.Priority.NORMAL]:
        items = items.filter(priority=priority)
    items = _period_filter(items, period)
    if sort in ['title', 'due_date', 'task_type', 'priority', 'status']:
        items = items.order_by(sort, 'due_time')

    today = timezone.localdate()
    stats = {
        'total': base_items.count(),
        'open': base_items.filter(status=Task.Status.OPEN).count(),
        'done': base_items.filter(status=Task.Status.DONE).count(),
        'deferred': base_items.filter(status=Task.Status.DEFERRED).count(),
        'urgent': base_items.filter(priority=Task.Priority.URGENT).count(),
        'due_today': base_items.filter(due_date=today).count(),
    }
    return render(request, 'books.html', {
        'items': items,
        'stats': stats,
        'q': q,
        'period': period,
        'sort': sort,
        'task_type': task_type,
        'status': status,
        'priority': priority,
        'official_types': [(value, label) for value, label in Task.Type.choices if value in BOOKS_FOLLOWUP_TYPES],
    })


@login_required
def book_create(request):
    messages.info(request, 'أضف الأعمال من صفحة المهام حتى يتم تصنيفها حسب التاريخ تلقائياً.')
    return redirect('planner:tasks')


@login_required
def book_edit(request, pk):
    return redirect('planner:task_edit', pk=pk)


@login_required
def book_delete(request, pk):
    return redirect('planner:task_delete', pk=pk)
