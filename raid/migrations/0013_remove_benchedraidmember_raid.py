# Generated by Django 3.0.1 on 2019-12-28 00:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('raid', '0012_auto_20191228_0016'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='benchedraidmember',
            name='raid',
        ),
    ]
