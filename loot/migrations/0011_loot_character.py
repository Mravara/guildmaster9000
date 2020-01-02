# Generated by Django 3.0.1 on 2019-12-30 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0022_auto_20191230_1156'),
        ('loot', '0010_auto_20191229_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='loot',
            name='character',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='members.Character'),
        ),
    ]