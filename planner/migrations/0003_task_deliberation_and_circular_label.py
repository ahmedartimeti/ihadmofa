# Generated manually for MOFA Smart Planner

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0002_task_sprint_2_1_choices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.CharField(choices=[('REVIEW', 'مطالعة'), ('OFFICIAL_BOOK', 'كتاب رسمي'), ('INCOMING', 'كتاب وارد'), ('OUTGOING', 'كتاب صادر'), ('CIRCULAR', 'إعمام'), ('FOLLOWUP', 'متابعة'), ('DELIBERATION', 'مداولة'), ('MEETING', 'اجتماع'), ('CALL', 'اتصال'), ('OTHER', 'أخرى')], default='OTHER', max_length=24),
        ),
    ]
