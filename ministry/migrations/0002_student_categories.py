from django.db import migrations, models


def copy_category_to_categories(apps, schema_editor):
    Student = apps.get_model('ministry', 'Student')
    for student in Student.objects.exclude(category__isnull=True):
        student.categories.add(student.category_id)


def copy_categories_to_category(apps, schema_editor):
    Student = apps.get_model('ministry', 'Student')
    for student in Student.objects.all():
        first = student.categories.first()
        if first:
            student.category_id = first.pk
            student.save(update_fields=['category'])


class Migration(migrations.Migration):

    dependencies = [
        ('ministry', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='students', to='ministry.category'),
        ),
        migrations.RunPython(copy_category_to_categories, reverse_code=copy_categories_to_category),
        migrations.RemoveField(
            model_name='student',
            name='category',
        ),
    ]