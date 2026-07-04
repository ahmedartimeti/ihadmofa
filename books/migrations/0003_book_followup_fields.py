# Generated manually for MOFA Smart Planner

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_book_sprint_visual_labels'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='issuing_entity',
            field=models.CharField(blank=True, max_length=160),
        ),
        migrations.AddField(
            model_name='book',
            name='required_action',
            field=models.CharField(blank=True, max_length=220),
        ),
        migrations.AddField(
            model_name='book',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='book_type',
            field=models.CharField(choices=[('OFFICIAL', 'كتاب رسمي'), ('INCOMING', 'كتاب وارد'), ('OUTGOING', 'كتاب صادر'), ('CIRCULAR', 'تعميم'), ('REVIEW', 'مطالعة'), ('FOLLOWUP', 'متابعة'), ('OTHER', 'أخرى')], max_length=20),
        ),
    ]
