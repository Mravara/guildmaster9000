# Generated by Django 3.0.1 on 2019-12-24 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loot', '0004_loot_prince_percentage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loot',
            old_name='prince_percentage',
            new_name='price_percentage',
        ),
    ]
