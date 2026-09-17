from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ministry', '0005_eventbudget_budgetitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='budgetitem',
            name='quantity',
        ),
        migrations.RenameField(
            model_name='budgetitem',
            old_name='unit_cost',
            new_name='cost',
        ),
        migrations.AddField(
            model_name='eventbudget',
            name='expected_participants',
            field=models.PositiveIntegerField(
                default=0,
                help_text='Expected number of participants for this budget',
            ),
        ),
    ]
