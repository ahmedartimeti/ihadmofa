from django import forms
from .models import Meeting

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ('title', 'meeting_date', 'meeting_time', 'location', 'notes')
        widgets = {'meeting_date': forms.DateInput(attrs={'type': 'date'}), 'meeting_time': forms.TimeInput(attrs={'type': 'time'})}
        labels = {'title':'عنوان الاجتماع','meeting_date':'التاريخ','meeting_time':'الوقت','location':'المكان','notes':'ملاحظات'}
