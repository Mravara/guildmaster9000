# Generated by Django 3.0.1 on 2020-03-29 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0033_member_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='comment',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
