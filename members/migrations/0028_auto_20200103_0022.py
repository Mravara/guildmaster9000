# Generated by Django 3.0.1 on 2020-01-03 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0027_auto_20200103_0019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='decaylog',
            name='affected_characters',
        ),
        migrations.AddField(
            model_name='decaylog',
            name='affected_members',
            field=models.ManyToManyField(related_name='decays', to='members.Member'),
        ),
    ]