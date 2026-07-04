from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'task_type', 'reference_number', 'priority', 'due_date', 'due_time', 'notes')
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'due_time': forms.TimeInput(attrs={'type': 'time'}),
        }
        labels = {
            'title': 'عنوان المهمة',
            'task_type': 'نوع العمل',
            'reference_number': 'رقم الكتاب إن وجد',
            'priority': 'الأولوية',
            'due_date': 'التاريخ',
            'due_time': 'الوقت',
            'notes': 'ملاحظات / الإجراء المطلوب',
        }
