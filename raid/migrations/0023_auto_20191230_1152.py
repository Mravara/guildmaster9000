# Generated by Django 3.0.1 on 2019-12-30 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0021_remove_member_member_class'),
        ('raid', '0022_auto_20191230_1151'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BenchedRaidMember',
            new_name='BenchedRaidCharacter',
        ),
    ]
