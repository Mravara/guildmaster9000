# Generated by Django 3.0.1 on 2019-12-26 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0010_auto_20191224_2245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='ep',
        ),
        migrations.RemoveField(
            model_name='member',
            name='gp',
        ),
    ]
