# Generated by Django 3.0.1 on 2020-01-05 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raid', '0027_remove_benchedraidcharacter_tmp_ep'),
    ]

    operations = [
        migrations.RenameField(
            model_name='raidcharacter',
            old_name='tmp_ep',
            new_name='earned_ep',
        ),
        migrations.AddField(
            model_name='benchedraidcharacter',
            name='earned_ep',
            field=models.FloatField(default=0),
        ),
    ]
