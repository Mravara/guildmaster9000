# Generated by Django 3.0.1 on 2020-03-13 22:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0029_remove_eplog_affected_characters'),
        ('officers', '0002_auto_20200313_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='target', to='members.Character'),
        ),
    ]
