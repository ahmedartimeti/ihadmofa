from datetime import time, timedelta

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils import timezone
from accounts.utils import is_viewer, restrict_queryset
from .forms import TaskForm
from .models import Task

WORK_END = time(14, 0)
OFFICIAL_TASK_TYPES = [
    Task.Type.REVIEW,
    Task.Type.INCOMING,
    Task.Type.OUTGOING,
    Task.Type.CIRCULAR,
    Task.Type.FOLLOWUP,
    Task.Type.DELIBERATION,
]


def _redirect_back(request, fallback='planner:tasks'):
    next_url = request.GET.get('next') or request.POST.get('next') or request.META.get('HTTP_REFERER')
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect(fallback)


def _can_write(request):
    if is_viewer(request.user):
        messages.error(request, 'صلاحية المشاهدة فقط لا تسمح بالتعديل.')
        return False
    return True


def _base_tasks(user):
    return restrict_queryset(Task.objects.all(), user)


def _is_overdue_today(now, task):
    return False


def _categorized_tasks(qs):
    today = timezone.localdate()
    tomorrow = today + timedelta(days=1)
    return {
        'past': qs.filter(due_date__lt=today),
        'today': qs.filter(due_date=today),
        'tomorrow': qs.filter(due_date=tomorrow),
        'future': qs.filter(due_date__gt=tomorrow),
    }


def _filtered_tasks(request):
    qs = _base_tasks(request.user)
    q = request.GET.get('q', '').strip()
    status = request.GET.get('status', '')
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(notes__icontains=q) | Q(reference_number__icontains=q))
    if status:
        qs = qs.filter(status=status)
    return qs, q, status


def _task_message_for_date(task):
    today = timezone.localdate()
    tomorrow = today + timedelta(days=1)
    if task.due_date < today:
        return 'تم حفظ المهمة ضمن مهام سابقة لأنها بتاريخ قديم.'
    if task.due_date == today:
        return 'تم حفظ المهمة ضمن مهام اليوم.'
    if task.due_date == tomorrow:
        return 'تم حفظ المهمة ضمن مهام يوم غد.'
    return 'تم حفظ المهمة ضمن مهام مستقبلية، وستنتقل تلقائياً عند حلول تاريخها.'


@login_required
def dashboard(request):
    return redirect('planner:tasks')


@login_required
def task_list(request):
    qs, q, status = _filtered_tasks(request)
    active_section = request.GET.get('section', 'today')
    if active_section not in ['past', 'today', 'tomorrow', 'future']:
        active_section = 'today'
    groups = _categorized_tasks(qs)
    book_count = qs.filter(task_type__in=OFFICIAL_TASK_TYPES).count()
    meeting_count = qs.filter(task_type=Task.Type.MEETING).count()
    return render(request, 'tasks.html', {
        'form': TaskForm(),
        'q': q,
        'status': status,
        'task_groups': groups,
        'active_section': active_section,
        'active_tasks': groups[active_section],
        'today_count': groups['today'].count(),
        'tomorrow_count': groups['tomorrow'].count(),
        'past_count': groups['past'].count(),
        'future_count': groups['future'].count(),
        'done_count': qs.filter(status=Task.Status.DONE).count(),
        'book_count': book_count,
        'meeting_count': meeting_count,
    })


@login_required
def task_create(request):
    if not _can_write(request):
        return _redirect_back(request)
    form = TaskForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        messages.success(request, _task_message_for_date(task))
    return _redirect_back(request)


@login_required
def task_edit(request, pk):
    task = get_object_or_404(_base_tasks(request.user), pk=pk)
    if not _can_write(request):
        return _redirect_back(request)
    form = TaskForm(request.POST or None, instance=task)
    if request.method == 'POST' and form.is_valid():
        edited = form.save()
        messages.success(request, _task_message_for_date(edited))
        return _redirect_back(request)
    qs, q, status = _filtered_tasks(request)
    active_section = request.GET.get('section', 'today')
    if active_section not in ['past', 'today', 'tomorrow', 'future']:
        active_section = 'today'
    groups = _categorized_tasks(qs)
    return render(request, 'tasks.html', {
        'task_groups': groups,
        'active_section': active_section,
        'active_tasks': groups[active_section],
        'form': form,
        'editing': task,
        'q': q,
        'status': status,
        'today_count': groups['today'].count(),
        'tomorrow_count': groups['tomorrow'].count(),
        'past_count': groups['past'].count(),
        'future_count': groups['future'].count(),
        'done_count': qs.filter(status=Task.Status.DONE).count(),
        'book_count': qs.filter(task_type__in=OFFICIAL_TASK_TYPES).count(),
        'meeting_count': qs.filter(task_type=Task.Type.MEETING).count(),
    })


@login_required
def task_delete(request, pk):
    task = get_object_or_404(_base_tasks(request.user), pk=pk)
    if _can_write(request):
        task.delete()
        messages.success(request, 'تم حذف المهمة.')
    return _redirect_back(request)


@login_required
def task_done(request, pk):
    task = get_object_or_404(_base_tasks(request.user), pk=pk)
    if _can_write(request):
        task.status = Task.Status.DONE
        task.save(update_fields=['status', 'updated_at'])
        messages.success(request, 'تم تثبيت المهمة كمنجزة.')
    return _redirect_back(request)


@login_required
def task_defer(request, pk):
    task = get_object_or_404(_base_tasks(request.user), pk=pk)
    if _can_write(request):
        task.status = Task.Status.DEFERRED
        task.save(update_fields=['status', 'updated_at'])
        messages.success(request, 'تم وضع المهمة بحالة مؤجلة دون تغيير تاريخها.')
    return _redirect_back(request)


@login_required
def task_remind(request, pk):
    task = get_object_or_404(_base_tasks(request.user), pk=pk)
    messages.info(request, f'تنبيه: {task.title} - {task.due_date} {task.due_time}')
    return _redirect_back(request)


@login_required
def send_today_plan_email(request):
    if request.method != 'POST':
        return redirect('planner:tasks')
    profile = getattr(request.user, 'profile', None)
    email = (getattr(profile, 'email_for_alerts', '') or request.user.email or '').strip()
    if not email:
        messages.error(request, 'لا يوجد إيميل مسجل في البروفايل لإرسال خطط اليوم.')
        return _redirect_back(request)

    today = timezone.localdate()
    tasks = _base_tasks(request.user).filter(due_date=today).order_by('due_time', 'title')
    employee = getattr(profile, 'full_name', '') or request.user.get_full_name() or request.user.username
    if tasks.exists():
        lines = [
            f'- {task.due_time.strftime("%H:%M")} | {task.title} | {task.get_task_type_display()} | {task.get_priority_display()} | {task.get_status_display()}'
            for task in tasks
        ]
    else:
        lines = ['لا توجد مهام مخططة لهذا اليوم.']

    subject = f'خطط اليوم - {today}'
    body_lines = [
        f'السيد/ة {employee}',
        '',
        f'خطط اليوم بتاريخ {today}:',
        '',
        *lines,
        '',
        'نظام المذكر اليومي للموظف',
    ]
    body = "\n".join(body_lines)
    try:
        send_mail(subject, body, getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@mofa.local'), [email], fail_silently=False)
        messages.success(request, f'تم إرسال خطط اليوم إلى: {email}')
    except Exception:
        messages.error(request, 'لم يتم إرسال البريد. تأكد من إعدادات البريد الإلكتروني SMTP في إعدادات النظام.')
    return _redirect_back(request)

