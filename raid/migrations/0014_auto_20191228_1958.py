# Generated by Django 3.0.1 on 2019-12-28 18:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raid', '0013_remove_benchedraidmember_raid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='benchedraidmember',
            name='start',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='raid',
            name='start',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='raidmember',
            name='start',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
