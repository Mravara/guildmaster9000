# Generated by Django 3.0.1 on 2019-12-30 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('raid', '0020_auto_20191230_1149'),
    ]

    operations = [
        migrations.RenameField(
            model_name='raid',
            old_name='benched_raid_members',
            new_name='benched_raid_characters',
        ),
    ]
