# Generated by Django 2.2.4 on 2020-01-08 05:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('sih', '0008_people_locationdatetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='LocationDateTime',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 8, 5, 5, 53, 306955, tzinfo=utc)),
        ),
    ]
