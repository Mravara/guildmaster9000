# Generated by Django 3.0.1 on 2019-12-24 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0005_auto_20191223_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_class',
            field=models.CharField(default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='item_subclass',
            field=models.CharField(default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='item_type_name',
            field=models.CharField(default='', max_length=256, null=True),
        ),
    ]
