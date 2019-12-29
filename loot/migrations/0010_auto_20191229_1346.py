# Generated by Django 3.0.1 on 2019-12-29 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0016_member_gp'),
        ('loot', '0009_loot_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loot',
            name='given_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='given_by', to='members.Member'),
        ),
    ]
