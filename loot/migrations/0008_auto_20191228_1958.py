# Generated by Django 3.0.1 on 2019-12-28 18:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loot', '0007_remove_loot_gp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loot',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]