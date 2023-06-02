# Generated by Django 3.0.1 on 2020-01-03 00:08

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('raid', '0025_auto_20200102_1103'),
        ('members', '0024_ep'),
    ]

    operations = [
        migrations.CreateModel(
            name='EPLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('affected_members', models.ManyToManyField(related_name='eplog', to='members.Member')),
                ('raid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='raid.Raid')),
            ],
        ),
        migrations.DeleteModel(
            name='EP',
        ),
    ]
