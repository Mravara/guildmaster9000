# Generated by Django 3.0.1 on 2019-12-24 23:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0007_iteminfo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='ep',
            new_name='gp',
        ),
    ]