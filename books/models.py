from django.conf import settings
from django.db import models
from django.utils import timezone


class Book(models.Model):
    class BookType(models.TextChoices):
        OFFICIAL = 'OFFICIAL', 'كتاب رسمي'
        INCOMING = 'INCOMING', 'كتاب وارد'
        OUTGOING = 'OUTGOING', 'كتاب صادر'
        CIRCULAR = 'CIRCULAR', 'تعميم'
        REVIEW = 'REVIEW', 'مطالعة'
        FOLLOWUP = 'FOLLOWUP', 'متابعة'
        OTHER = 'OTHER', 'أخرى'

    class Status(models.TextChoices):
        OPEN = 'OPEN', 'متبقي'
        DONE = 'DONE', 'منجز'
        DEFERRED = 'DEFERRED', 'مؤجل'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='books')
    title = models.CharField(max_length=220)
    book_type = models.CharField(max_length=20, choices=BookType.choices)
    reference_number = models.CharField(max_length=80, blank=True)
    issuing_entity = models.CharField(max_length=160, blank=True)
    required_action = models.CharField(max_length=220, blank=True)
    date = models.DateField(default=timezone.localdate)
    due_date = models.DateField(blank=True, null=True)
    priority = models.CharField(max_length=20, default='NORMAL', choices=[('NORMAL','عادية'),('IMPORTANT','مهمة'),('URGENT','عاجلة')])
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', 'title']

    def __str__(self):
        return self.title
