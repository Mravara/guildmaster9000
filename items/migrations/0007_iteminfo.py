# Generated by Django 3.0.1 on 2019-12-24 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0006_auto_20191224_1219'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot', models.CharField(max_length=128)),
                ('slot_value', models.FloatField()),
                ('slot_ref', models.IntegerField(choices=[(0, 'Twohandmelee'), (1, 'Rangedhunter'), (2, 'Twohandcaster'), (3, 'Onehandmelee'), (4, 'Onehandcaster'), (5, 'Shieldmelee'), (6, 'Head'), (7, 'Chest'), (8, 'Legs'), (9, 'Shoulder'), (10, 'Hands'), (11, 'Waist'), (12, 'Feet'), (13, 'Twohandhunter'), (14, 'Wand'), (15, 'Shieldcaster'), (16, 'Trinket'), (17, 'Wrist'), (18, 'Neck'), (19, 'Back'), (20, 'Finger'), (21, 'Rangedmelee'), (22, 'Onehandhunter'), (23, 'Offhandcaster'), (24, 'Relic')])),
            ],
        ),
    ]
