# Generated manually for MOFA Smart Planner Sprint 2.1

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.CharField(choices=[('REVIEW', 'مطالعة'), ('OFFICIAL_BOOK', 'كتاب رسمي'), ('INCOMING', 'كتاب وارد'), ('OUTGOING', 'كتاب صادر'), ('CIRCULAR', 'تعميم'), ('FOLLOWUP', 'متابعة'), ('MEETING', 'اجتماع'), ('CALL', 'اتصال'), ('OTHER', 'أخرى')], default='OTHER', max_length=20),
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
