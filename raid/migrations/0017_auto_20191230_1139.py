# Generated by Django 3.0.1 on 2019-12-30 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0021_remove_member_member_class'),
        ('raid', '0016_auto_20191230_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raid',
            name='leader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='leader', to='members.Member'),
        ),
    ]
