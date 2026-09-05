from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ministry', '0003_create_groups'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='expected_attendance',
            new_name='attended_students',
        ),
        migrations.DeleteModel(
            name='Attendance',
        ),
    ]
