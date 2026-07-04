from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash, views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Count
from django.shortcuts import redirect, render
from django.utils import timezone
from .forms import (
    DataClearForm,
    ProfileForm,
    ProfilePasswordChangeForm,
    PublicPasswordRecoveryForm,
    RecoveryPasswordChangeForm,
    EmailOrUsernameAuthenticationForm,
    RegisterForm,
    SecureActionForm,
    SettingsRecoveryForm,
    SettingsUnlockForm,
)
from .models import UserProfile


class LoginView(auth_views.LoginView):
    template_name = 'login.html'
    authentication_form = EmailOrUsernameAuthenticationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault('register_form', RegisterForm())
        context.setdefault('recovery_form', PublicPasswordRecoveryForm())
        return context


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'تم إنشاء الحساب وتسجيل الدخول بنجاح.')
            return redirect('planner:tasks')
    else:
        form = RegisterForm()
    return render(request, 'login.html', {'form': EmailOrUsernameAuthenticationForm(), 'register_form': form, 'recovery_form': PublicPasswordRecoveryForm(), 'show_register': True})


def recover_password(request):
    if request.method != 'POST':
        return redirect('accounts:login')

    form = PublicPasswordRecoveryForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'تم تغيير الرمز السري. يمكنك تسجيل الدخول الآن.')
        return redirect('accounts:login')

    return render(request, 'login.html', {
        'form': EmailOrUsernameAuthenticationForm(),
        'register_form': RegisterForm(),
        'recovery_form': form,
        'show_recovery': True,
    })

def account_logout(request):
    logout(request)
    messages.success(request, 'تم تسجيل الخروج.')
    return redirect('accounts:login')


def _profile_for(user):
    profile, _ = UserProfile.objects.get_or_create(
        user=user,
        defaults={'full_name': user.get_full_name() or user.username, 'department': ''},
    )
    return profile


def _settings_unlocked(request):
    return request.session.get('settings_unlocked_for') == request.user.pk


def _unlock_settings(request):
    request.session['settings_unlocked_for'] = request.user.pk


def _is_admin_user(user):
    profile = getattr(user, 'profile', None)
    return user.is_superuser or getattr(profile, 'role', None) == UserProfile.Role.ADMIN


def _clear_user_data(user, scope):
    from books.models import Book
    from meetings.models import Meeting
    from notifications.models import Notification
    from planner.models import Task
    from reports.models import DailyReport

    today = timezone.localdate()
    task_qs = Task.objects.filter(user=user)
    report_qs = DailyReport.objects.filter(user=user)

    if scope == 'all':
        task_qs.delete()
        Book.objects.filter(user=user).delete()
        Meeting.objects.filter(user=user).delete()
        Notification.objects.filter(user=user).delete()
        report_qs.delete()
        return
    if scope == 'reports':
        report_qs.delete()
        return
    if scope == 'today':
        task_qs.filter(due_date=today).delete()
        return
    if scope == 'week':
        start = today - timedelta(days=today.weekday())
        task_qs.filter(due_date__gte=start, due_date__lte=start + timedelta(days=6)).delete()
        return
    if scope == 'month':
        task_qs.filter(due_date__year=today.year, due_date__month=today.month).delete()
        return
    if scope == 'year':
        task_qs.filter(due_date__year=today.year).delete()


@login_required
def profile_settings(request):
    profile = _profile_for(request.user)
    recovery_verified = request.session.get('settings_recovery_verified_for') == request.user.pk

    if not _settings_unlocked(request):
        unlock_form = SettingsUnlockForm(request.POST or None, prefix='unlock')
        recovery_form = SettingsRecoveryForm(request.POST or None, prefix='recovery')
        recovery_password_form = RecoveryPasswordChangeForm(request.user, request.POST or None, prefix='recovery_password')

        if request.method == 'POST' and request.POST.get('action') == 'unlock':
            if unlock_form.is_valid() and request.user.check_password(unlock_form.cleaned_data['password']):
                _unlock_settings(request)
                messages.success(request, 'تم فتح الإعدادات.')
                return redirect('settings')
            messages.error(request, 'كلمة المرور غير صحيحة.')

        if request.method == 'POST' and request.POST.get('action') == 'recover':
            if recovery_form.is_valid():
                school = recovery_form.cleaned_data['first_school'].strip()
                city = recovery_form.cleaned_data['birth_city'].strip()
                if profile.first_school.strip() == school and profile.birth_city.strip() == city:
                    request.session['settings_recovery_verified_for'] = request.user.pk
                    messages.success(request, 'تم التحقق من الهوية. يمكنك تغيير كلمة المرور الآن.')
                    return redirect('settings')
                messages.error(request, 'لم يتم التحقق من الهوية.')

        if request.method == 'POST' and request.POST.get('action') == 'recovery_password' and recovery_verified:
            if recovery_password_form.is_valid():
                recovery_password_form.save()
                update_session_auth_hash(request, request.user)
                _unlock_settings(request)
                request.session.pop('settings_recovery_verified_for', None)
                messages.success(request, 'تم تغيير كلمة المرور وفتح الإعدادات.')
                return redirect('settings')

        return render(request, 'settings_gate.html', {
            'unlock_form': unlock_form,
            'recovery_form': recovery_form,
            'recovery_password_form': recovery_password_form,
            'recovery_verified': recovery_verified,
        })

    profile_form = ProfileForm(instance=profile)
    password_form = ProfilePasswordChangeForm(request.user)
    clear_form = DataClearForm(prefix='clear')
    delete_form = SecureActionForm(prefix='delete')
    is_admin = _is_admin_user(request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action and action.startswith('admin_'):
            if not is_admin:
                messages.error(request, 'ليست لديك صلاحية تنفيذ هذا الإجراء.')
                return redirect('settings')

            target = User.objects.filter(pk=request.POST.get('user_id')).first()
            if not target:
                messages.error(request, 'لم يتم العثور على المستخدم.')
                return redirect('settings')

            if target == request.user and action in {'admin_block_user', 'admin_delete_user'}:
                messages.error(request, 'لا يمكن حظر أو حذف حسابك الحالي من هنا.')
                return redirect('settings')

            if action == 'admin_block_user':
                target.is_active = False
                target.save(update_fields=['is_active'])
                messages.success(request, 'تم حظر المستخدم.')
            elif action == 'admin_unblock_user':
                target.is_active = True
                target.save(update_fields=['is_active'])
                messages.success(request, 'تم رفع الحظر عن المستخدم.')
            elif action == 'admin_clear_user':
                scope = request.POST.get('scope', 'all')
                allowed_scopes = {choice[0] for choice in DataClearForm.base_fields['scope'].choices}
                if scope not in allowed_scopes:
                    messages.error(request, 'نطاق المسح غير صحيح.')
                    return redirect('settings')
                _clear_user_data(target, scope)
                messages.success(request, 'تم مسح بيانات المستخدم حسب النطاق المحدد.')
            elif action == 'admin_delete_user':
                target.delete()
                messages.success(request, 'تم حذف المستخدم وبياناته المرتبطة.')
            elif action == 'admin_role_user':
                role = request.POST.get('role')
                allowed_roles = {choice[0] for choice in UserProfile.Role.choices}
                if role not in allowed_roles:
                    messages.error(request, 'الصلاحية غير صحيحة.')
                    return redirect('settings')
                target_profile = _profile_for(target)
                target_profile.role = role
                target_profile.save(update_fields=['role'])
                messages.success(request, 'تم تحديث صلاحية المستخدم.')
            return redirect('settings')

        if action == 'profile':
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'تم حفظ بيانات البروفايل.')
                return redirect('settings')
        elif action == 'password':
            password_form = ProfilePasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'تم تغيير كلمة المرور.')
                return redirect('settings')
        elif action == 'clear':
            clear_form = DataClearForm(request.POST, prefix='clear')
            if clear_form.is_valid() and request.user.check_password(clear_form.cleaned_data['password']):
                _clear_user_data(request.user, clear_form.cleaned_data['scope'])
                messages.success(request, 'تم مسح البيانات حسب النطاق المحدد.')
                return redirect('settings')
            messages.error(request, 'لم يتم المسح. تأكد من كلمة المرور.')
        elif action == 'delete_account':
            delete_form = SecureActionForm(request.POST, prefix='delete')
            if delete_form.is_valid() and request.user.check_password(delete_form.cleaned_data['password']):
                with transaction.atomic():
                    user = User.objects.select_for_update().get(pk=request.user.pk)
                    logout(request)
                    user.delete()
                messages.success(request, 'تم حذف الحساب وكل البيانات المرتبطة به.')
                return redirect('accounts:login')
            messages.error(request, 'لم يتم حذف الحساب. كلمة المرور غير صحيحة.')

    admin_users = []
    if is_admin:
        user_queryset = User.objects.select_related('profile').annotate(task_count=Count('tasks')).order_by('username')
        for member in user_queryset:
            admin_users.append({
                'user': member,
                'profile': _profile_for(member),
                'task_count': member.task_count,
            })

    return render(request, 'settings.html', {
        'profile_form': profile_form,
        'password_form': password_form,
        'clear_form': clear_form,
        'delete_form': delete_form,
        'is_admin': is_admin,
        'admin_users': admin_users,
        'role_choices': UserProfile.Role.choices,
        'clear_scopes': DataClearForm.base_fields['scope'].choices,
    })
