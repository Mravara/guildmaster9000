# Generated by Django 3.0.1 on 2019-12-22 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='rank',
            field=models.IntegerField(choices=[(0, 'Member'), (10, 'Raid Leader'), (100, 'Officer'), (1000, 'Admin')], default=0),
        ),
    ]
