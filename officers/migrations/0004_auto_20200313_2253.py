# Generated by Django 3.0.1 on 2020-03-13 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('officers', '0003_auto_20200313_2252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='value',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
