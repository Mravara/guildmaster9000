# Generated by Django 3.0.1 on 2020-04-02 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raid', '0030_auto_20200402_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raid',
            name='start',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]