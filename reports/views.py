from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from accounts.utils import restrict_queryset
from planner.models import Task


def period_queryset(qs, period):
    today = timezone.localdate()
    if period == 'weekly':
        start = today - timedelta(days=today.weekday())
        return qs.filter(due_date__gte=start, due_date__lte=start + timedelta(days=6))
    if period == 'monthly':
        return qs.filter(due_date__year=today.year, due_date__month=today.month)
    if period == 'yearly':
        return qs.filter(due_date__year=today.year)
    return qs.filter(due_date=today)

@login_required
def reports_view(request):
    period = request.GET.get('period', 'daily')
    tasks = period_queryset(restrict_queryset(Task.objects.all(), request.user), period)
    done = tasks.filter(status=Task.Status.DONE).count()
    deferred = tasks.filter(status=Task.Status.DEFERRED).count()
    open_count = tasks.exclude(status__in=[Task.Status.DONE, Task.Status.DEFERRED, Task.Status.CANCELLED]).count()
    urgent = tasks.filter(priority=Task.Priority.URGENT).count()
    important = tasks.filter(priority=Task.Priority.IMPORTANT).count()
    normal = tasks.filter(priority=Task.Priority.NORMAL).count()
    period_map = {'daily': 'today', 'weekly': 'week', 'monthly': 'month', 'yearly': 'year'}
    books_period = period_map.get(period, 'today')
    type_counts = [
        {'key': 'review', 'label': 'عدد المطالعة', 'value': tasks.filter(task_type=Task.Type.REVIEW).count(), 'url': f'/books/?period={books_period}&type={Task.Type.REVIEW}'},
        {'key': 'books_all', 'label': 'عدد الكتب', 'value': tasks.filter(task_type__in=[Task.Type.INCOMING, Task.Type.OUTGOING]).count(), 'url': f'/books/?period={books_period}'},
        {'key': 'incoming', 'label': 'عدد الكتب الوارد', 'value': tasks.filter(task_type=Task.Type.INCOMING).count(), 'url': f'/books/?period={books_period}&type={Task.Type.INCOMING}'},
        {'key': 'outgoing', 'label': 'عدد الكتب الصادر', 'value': tasks.filter(task_type=Task.Type.OUTGOING).count(), 'url': f'/books/?period={books_period}&type={Task.Type.OUTGOING}'},
        {'key': 'circular', 'label': 'عدد الإعمام', 'value': tasks.filter(task_type=Task.Type.CIRCULAR).count(), 'url': f'/books/?period={books_period}&type={Task.Type.CIRCULAR}'},
        {'key': 'followup', 'label': 'عدد المتابعة', 'value': tasks.filter(task_type=Task.Type.FOLLOWUP).count(), 'url': f'/books/?period={books_period}&type={Task.Type.FOLLOWUP}'},
        {'key': 'deliberation', 'label': 'عدد المداولة', 'value': tasks.filter(task_type=Task.Type.DELIBERATION).count(), 'url': f'/books/?period={books_period}&type={Task.Type.DELIBERATION}'},
        {'key': 'meeting', 'label': 'عدد الاجتماع', 'value': tasks.filter(task_type=Task.Type.MEETING).count(), 'url': f'/books/?period={books_period}&type={Task.Type.MEETING}'},
        {'key': 'call', 'label': 'عدد الاتصال', 'value': tasks.filter(task_type=Task.Type.CALL).count(), 'url': f'/books/?period={books_period}&type={Task.Type.CALL}'},
        {'key': 'other', 'label': 'عدد الأخرى', 'value': tasks.filter(task_type=Task.Type.OTHER).count(), 'url': f'/books/?period={books_period}&type={Task.Type.OTHER}'},
    ]
    max_type_count = max([item['value'] for item in type_counts] or [1]) or 1
    for item in type_counts:
        item['height'] = max(6, round((item['value'] / max_type_count) * 120)) if item['value'] else 6

    def degrees(parts):
        total = sum(parts) or 1
        current = 0
        output = []
        for value in parts:
            start = current
            current += round((value / total) * 360, 2)
            output.append((start, current))
        return output

    done_deg, open_deg, deferred_deg = degrees([done, open_count, deferred])
    urgent_deg, important_deg, normal_deg = degrees([urgent, important, normal])
    stats = {
        'total': tasks.count(),
        'done': done,
        'open': open_count,
        'deferred': deferred,
        'urgent': urgent,
        'important': important,
        'normal': normal,
        'completion_donut': f"conic-gradient(#16a34a {done_deg[0]}deg {done_deg[1]}deg, #2563eb {open_deg[0]}deg {open_deg[1]}deg, #f4b62a {deferred_deg[0]}deg {deferred_deg[1]}deg)",
        'priority_donut': f"conic-gradient(#c53b47 {urgent_deg[0]}deg {urgent_deg[1]}deg, #f4b62a {important_deg[0]}deg {important_deg[1]}deg, #16a34a {normal_deg[0]}deg {normal_deg[1]}deg)",
        'done_url': f'/books/?period={books_period}&status={Task.Status.DONE}',
        'open_url': f'/books/?period={books_period}&status={Task.Status.OPEN}',
        'deferred_url': f'/books/?period={books_period}&status={Task.Status.DEFERRED}',
        'urgent_url': f'/books/?period={books_period}&priority={Task.Priority.URGENT}',
        'important_url': f'/books/?period={books_period}&priority={Task.Priority.IMPORTANT}',
        'normal_url': f'/books/?period={books_period}&priority={Task.Priority.NORMAL}',
    }
    return render(request, 'reports.html', {'stats': stats, 'period': period, 'type_counts': type_counts})

@login_required
def reports_export(request):
    period = request.GET.get('period', 'daily')
    tasks = period_queryset(restrict_queryset(Task.objects.all(), request.user), period)
    rows = ''.join(f'<tr><td>{t.due_date}</td><td>{t.due_time}</td><td>{t.title}</td><td>{t.get_task_type_display()}</td><td>{t.get_priority_display()}</td><td>{t.get_status_display()}</td></tr>' for t in tasks)
    profile = getattr(request.user, 'profile', None)
    employee = profile.full_name if profile else request.user.username
    department = profile.department if profile else ''
    html = f'''<html dir="rtl"><head><meta charset="utf-8"><style>@page{{size:A4 landscape;margin:10mm}} body{{font-family:Arial}} table{{width:100%;border-collapse:collapse}} td,th{{border:1px solid #999;padding:7px;text-align:right}}</style></head><body><h2>تقرير {period}</h2><table><tr><th>التاريخ</th><th>الوقت</th><th>العنوان</th><th>النوع</th><th>الأهمية</th><th>الحالة</th></tr>{rows}</table><p>الموظف: {employee}</p><p>القسم/الدائرة: {department}</p><p>تاريخ التصدير: {timezone.localdate()}</p></body></html>'''
    response = HttpResponse('﻿' + html, content_type='application/vnd.ms-excel; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="mofa-report-{period}.xls"'
    return response
