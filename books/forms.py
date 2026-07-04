from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'book_type', 'reference_number', 'issuing_entity', 'required_action', 'date', 'due_date', 'priority', 'status', 'notes')
        widgets = {'date': forms.DateInput(attrs={'type': 'date'}), 'due_date': forms.DateInput(attrs={'type': 'date'})}
        labels = {
            'title': 'عنوان المتابعة',
            'book_type': 'نوع المتابعة',
            'reference_number': 'الرقم إن وجد',
            'issuing_entity': 'الجهة / الدائرة',
            'required_action': 'ماذا مطلوب؟',
            'date': 'تاريخ الكتاب',
            'due_date': 'متى أتابعها؟',
            'priority': 'الأولوية',
            'status': 'الحالة',
            'notes': 'ملاحظات',
        }
