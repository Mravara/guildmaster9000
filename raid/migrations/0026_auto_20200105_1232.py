# Generated by Django 3.0.1 on 2020-01-05 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raid', '0025_auto_20200102_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='benchedraidcharacter',
            name='tmp_ep',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='raidcharacter',
            name='tmp_ep',
            field=models.FloatField(default=0),
        ),
    ]
