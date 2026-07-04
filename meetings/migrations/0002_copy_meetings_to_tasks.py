# Generated manually for MOFA Smart Planner

from django.db import migrations


def copy_meetings_to_tasks(apps, schema_editor):
    Meeting = apps.get_model('meetings', 'Meeting')
    Task = apps.get_model('planner', 'Task')
    status_map = {
        'OPEN': 'OPEN',
        'DONE': 'DONE',
        'DEFERRED': 'DEFERRED',
        'CANCELLED': 'CANCELLED',
    }
    for meeting in Meeting.objects.all():
        exists = Task.objects.filter(
            user_id=meeting.user_id,
            title=meeting.title,
            task_type='MEETING',
            due_date=meeting.meeting_date,
            due_time=meeting.meeting_time,
        ).exists()
        if exists:
            continue
        notes = meeting.notes or ''
        if meeting.location:
            notes = (notes + '\n' if notes else '') + f'المكان: {meeting.location}'
        Task.objects.create(
            user_id=meeting.user_id,
            title=meeting.title,
            task_type='MEETING',
            reference_number='',
            priority='NORMAL',
            status=status_map.get(meeting.status, 'OPEN'),
            due_date=meeting.meeting_date,
            due_time=meeting.meeting_time,
            notes=notes,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0004_remove_official_book_choice'),
        ('meetings', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(copy_meetings_to_tasks, migrations.RunPython.noop),
    ]
