# Generated by Django 3.0.2 on 2020-01-15 04:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sih', '0018_auto_20200113_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personinneed',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]