from django import forms
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm, UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class RegisterForm(UserCreationForm):
    full_name = forms.CharField(label='الاسم الكامل')
    department = forms.CharField(label='الدائرة')
    section = forms.CharField(label='القسم', required=False)
    job_title = forms.CharField(label='العنوان الوظيفي', required=False)
    email_for_alerts = forms.EmailField(label='إيميل التنبيهات', required=False)
    first_school = forms.CharField(label='اسم أول مدرسة ابتدائية')
    birth_city = forms.CharField(label='المدينة التي ولد فيها')

    class Meta:
        model = User
        fields = ('username', 'full_name', 'department', 'section', 'job_title', 'email_for_alerts', 'password1', 'password2', 'first_school', 'birth_city')

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = user.profile
        profile.full_name = self.cleaned_data['full_name']
        profile.department = self.cleaned_data['department']
        profile.section = self.cleaned_data.get('section', '')
        profile.job_title = self.cleaned_data.get('job_title', '')
        profile.email_for_alerts = self.cleaned_data.get('email_for_alerts', '')
        profile.first_school = self.cleaned_data.get('first_school', '')
        profile.birth_city = self.cleaned_data.get('birth_city', '')
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
