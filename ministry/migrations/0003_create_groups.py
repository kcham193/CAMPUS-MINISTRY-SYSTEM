from django.db import migrations


ADMIN_GROUP = 'Admins'
VIEWER_GROUP = 'Viewers'


def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    User = apps.get_model('auth', 'User')

    admin_group, _ = Group.objects.get_or_create(name=ADMIN_GROUP)
    Group.objects.get_or_create(name=VIEWER_GROUP)

    for superuser in User.objects.filter(is_superuser=True):
        superuser.groups.add(admin_group)


def remove_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=[ADMIN_GROUP, VIEWER_GROUP]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('ministry', '0002_student_categories'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(create_groups, reverse_code=remove_groups),
    ]