# Generated by Django 3.0.1 on 2020-03-29 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0032_auto_20200329_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='comment',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
