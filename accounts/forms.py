import re

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm, UserCreationForm, UsernameField
from django.contrib.auth.models import User
from .models import UserProfile


class EmailOrUsernameAuthenticationForm(AuthenticationForm):
    username = UsernameField(label='اسم المستخدم أو الإيميل')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            login_value = username.strip()
            auth_username = login_value

            if '@' in login_value:
                user = User.objects.filter(email__iexact=login_value).first()
                if user is None:
                    profile = UserProfile.objects.select_related('user').filter(email_for_alerts__iexact=login_value).first()
                    user = profile.user if profile else None
                if user is not None:
                    auth_username = user.get_username()

            self.user_cache = authenticate(self.request, username=auth_username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class RegisterForm(UserCreationForm):
    username = forms.CharField(required=False, widget=forms.HiddenInput)
    full_name = forms.CharField(label='الاسم الكامل')
    department = forms.CharField(label='الدائرة')
    section = forms.CharField(label='القسم', required=False)
    job_title = forms.CharField(label='العنوان الوظيفي', required=False)
    email_for_alerts = forms.EmailField(label='إيميل التنبيهات', required=False)
    first_school = forms.CharField(label='اسم أول مدرسة ابتدائية')
    birth_city = forms.CharField(label='المدينة التي ولد فيها')
    photo = forms.ImageField(label='صورة الموظف عند الحاجة', required=False)

    def clean_username(self):
        username = (self.cleaned_data.get('username') or '').strip()
        email = (self.cleaned_data.get('email_for_alerts') or '').strip()
        full_name = (self.cleaned_data.get('full_name') or '').strip()

        if not username:
            username = email.split('@')[0] if email else full_name
        username = re.sub(r'[^A-Za-z0-9_.@+-]+', '_', username).strip('_.')
        if not username:
            username = 'employee'

        candidate = username[:140]
        suffix = 1
        while User.objects.filter(username__iexact=candidate).exists():
            suffix += 1
            candidate = f'{username[:130]}_{suffix}'
        return candidate

    class Meta:
        model = User
        fields = ('username', 'full_name', 'department', 'section', 'job_title', 'email_for_alerts', 'password1', 'password2', 'first_school', 'birth_city', 'photo')

    def save(self, commit=True):
        user = super().save(commit=commit)
        user.email = self.cleaned_data.get('email_for_alerts', '')
        if commit:
            user.save(update_fields=['email'])
        profile = user.profile
        profile.full_name = self.cleaned_data['full_name']
        profile.department = self.cleaned_data['department']
        profile.section = self.cleaned_data.get('section', '')
        profile.job_title = self.cleaned_data.get('job_title', '')
        profile.email_for_alerts = self.cleaned_data.get('email_for_alerts', '')
        profile.first_school = self.cleaned_data.get('first_school', '')
        profile.birth_city = self.cleaned_data.get('birth_city', '')
        if self.cleaned_data.get('photo'):
            profile.photo = self.cleaned_data['photo']
        if commit:
            profile.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('full_name', 'department', 'section', 'job_title', 'email_for_alerts', 'photo')
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'profile-photo-input'}),
        }
        labels = {
            'full_name': 'الاسم',
            'department': 'الدائرة',
            'section': 'القسم',
            'job_title': 'العنوان الوظيفي',
            'email_for_alerts': 'الإيميل',
            'photo': 'الصورة الشخصية',
        }


class SettingsUnlockForm(forms.Form):
    password = forms.CharField(label='كلمة المرور', widget=forms.PasswordInput)


class SettingsRecoveryForm(forms.Form):
    first_school = forms.CharField(label='اسم أول مدرسة ابتدائية')
    birth_city = forms.CharField(label='المدينة التي ولد فيها')


class SecureActionForm(forms.Form):
    password = forms.CharField(label='كلمة المرور', widget=forms.PasswordInput)


class DataClearForm(SecureActionForm):
    scope = forms.ChoiceField(label='نطاق المسح', choices=[
        ('all', 'الكل'),
        ('today', 'اليوم'),
        ('week', 'الأسبوع'),
        ('month', 'الشهر'),
        ('year', 'السنة'),
        ('reports', 'التقارير'),
    ])


class ProfilePasswordChangeForm(PasswordChangeForm):
    pass


class RecoveryPasswordChangeForm(SetPasswordForm):
    pass


class PublicPasswordRecoveryForm(forms.Form):
    identifier = forms.CharField(label='اسم المستخدم أو الإيميل')
    first_school = forms.CharField(label='اسم أول مدرسة ابتدائية')
    birth_city = forms.CharField(label='المدينة التي ولدت فيها')
    new_password1 = forms.CharField(label='الرمز السري الجديد', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='تأكيد الرمز السري الجديد', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        identifier = cleaned_data.get('identifier', '').strip()
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')

        if password1 and password2 and password1 != password2:
            self.add_error('new_password2', 'الرمزان غير متطابقين.')

        user = None
        if identifier:
            user = User.objects.filter(username__iexact=identifier).first()
            if user is None and '@' in identifier:
                user = User.objects.filter(email__iexact=identifier).first()
            if user is None and '@' in identifier:
                profile = UserProfile.objects.select_related('user').filter(email_for_alerts__iexact=identifier).first()
                user = profile.user if profile else None

        if user is None:
            self.add_error('identifier', 'لم يتم العثور على الحساب.')
            return cleaned_data

        profile = getattr(user, 'profile', None)
        school = cleaned_data.get('first_school', '').strip()
        city = cleaned_data.get('birth_city', '').strip()
        if profile is None or profile.first_school.strip() != school or profile.birth_city.strip() != city:
            self.add_error('birth_city', 'بيانات التحقق غير صحيحة.')
            return cleaned_data

        cleaned_data['user'] = user
        return cleaned_data

    def save(self):
        user = self.cleaned_data['user']
        user.set_password(self.cleaned_data['new_password1'])
        user.save(update_fields=['password'])
        return user
