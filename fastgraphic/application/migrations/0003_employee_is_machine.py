# Generated by Django 3.1.4 on 2021-01-21 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_auto_20210119_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='is_machine',
            field=models.BooleanField(default=False),
        ),
    ]