# Generated by Django 3.0.1 on 2019-12-29 15:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0016_member_gp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Decay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage', models.FloatField()),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='members.Member')),
            ],
        ),
    ]
