# Generated by Django 2.2.4 on 2020-01-04 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sih', '0003_auto_20200104_2222'),
    ]

    operations = [
        migrations.AddField(
            model_name='people',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='people',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]