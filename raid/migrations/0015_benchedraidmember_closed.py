# Generated by Django 3.0.1 on 2019-12-28 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raid', '0014_auto_20191228_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='benchedraidmember',
            name='closed',
            field=models.BooleanField(default=False),
        ),
    ]
