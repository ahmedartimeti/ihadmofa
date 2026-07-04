# Generated manually for visual label cleanup

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_type',
            field=models.CharField(choices=[('OFFICIAL', 'كتاب رسمي'), ('INCOMING', 'كتاب وارد'), ('OUTGOING', 'كتاب صادر'), ('CIRCULAR', 'تعميم'), ('REVIEW', 'مطالعة')], max_length=20),
        ),
        migrations.AlterField(
            model_name='book',
            name='priority',
            field=models.CharField(choices=[('NORMAL', 'عادية'), ('IMPORTANT', 'مهمة'), ('URGENT', 'عاجلة')], default='NORMAL', max_length=20),
        ),
        migrations.AlterField(
            model_name='book',
            name='status',
            field=models.CharField(choices=[('OPEN', 'متبقي'), ('DONE', 'منجز'), ('DEFERRED', 'مؤجل')], default='OPEN', max_length=20),
        ),
    ]
