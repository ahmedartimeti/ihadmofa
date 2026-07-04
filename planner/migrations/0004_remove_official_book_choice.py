# Generated manually for MOFA Smart Planner

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0003_task_deliberation_and_circular_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.CharField(choices=[('REVIEW', 'مطالعة'), ('INCOMING', 'كتاب وارد'), ('OUTGOING', 'كتاب صادر'), ('CIRCULAR', 'إعمام'), ('FOLLOWUP', 'متابعة'), ('DELIBERATION', 'مداولة'), ('MEETING', 'اجتماع'), ('CALL', 'اتصال'), ('OTHER', 'أخرى')], default='OTHER', max_length=24),
        ),
    ]
