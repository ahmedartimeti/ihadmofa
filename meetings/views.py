from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from planner.models import Task


@login_required
def meeting_list(request):
    return redirect(f'/books/?period=all&type={Task.Type.MEETING}')


@login_required
def meeting_create(request):
    messages.info(request, 'أضف الموعد من صفحة المهام واختر نوع العمل: اجتماع.')
    return redirect('planner:tasks')


@login_required
def meeting_edit(request, pk):
    return redirect('planner:task_edit', pk=pk)


@login_required
def meeting_done(request, pk):
    return redirect('planner:task_done', pk=pk)


@login_required
def meeting_defer(request, pk):
    return redirect('planner:task_defer', pk=pk)


@login_required
def meeting_delete(request, pk):
    return redirect('planner:task_delete', pk=pk)
