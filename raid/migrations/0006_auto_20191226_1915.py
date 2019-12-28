# Generated by Django 3.0.1 on 2019-12-26 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0013_member_ep'),
        ('raid', '0005_remove_raid_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='raid',
            name='raid_members',
            field=models.ManyToManyField(null=True, to='members.Member'),
        ),
        migrations.AlterField(
            model_name='raid',
            name='leader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='leader', to='members.Member'),
        ),
    ]