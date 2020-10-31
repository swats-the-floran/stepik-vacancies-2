from django.contrib.auth import get_user_model
from django.db import migrations

from django.conf import settings
from vacancies.models import Company
from vacancies.population_script import populate


def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version

    populate()

    companies = Company.objects.all()
    user_model = get_user_model()

    for company in companies:
        user_ = user_model.objects.create_user(
            username=f'{company.name}_owner',
            password='1234567Q',
        )
        user_.first_name = company.name
        user_.last_name = 'owner'
        user_.save()
        company.owner = user_
        company.save()


def reverse_func(apps, schema_editor):
    # forwards_func() creates two Country instances,
    # so reverse_func() should delete them.

    pass  # i really don't have time for this right now


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vacancies', '0002_auto_20201031_1742'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
