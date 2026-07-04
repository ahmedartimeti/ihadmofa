# Generated manually for IHAD production release 2.2

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0004_remove_official_book_choice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.CharField(choices=[('REVIEW', 'مطالعة'), ('INCOMING', 'كتاب وارد'), ('OUTGOING', 'كتاب صادر'), ('CIRCULAR', 'إعمام'), ('DELIBERATION', 'مداولة'), ('FOLLOWUP', 'متابعة'), ('MEETING', 'اجتماع'), ('CALL', 'اتصال'), ('OTHER', 'أخرى')], default='OTHER', max_length=24),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('NORMAL', 'عادي'), ('IMPORTANT', 'مهم'), ('URGENT', 'عاجل')], default='NORMAL', max_length=20),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('OPEN', 'مفتوح'), ('DONE', 'منجز'), ('DEFERRED', 'مؤجل'), ('OVERDUE', 'متأخر'), ('CANCELLED', 'ملغاة')], default='OPEN', max_length=20),
        ),
    ]
