# Generated by Django 3.0 on 2022-04-30 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gdapp', '0009_property_reward_soldproperty'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='is_popular',
            field=models.BooleanField(default=False),
        ),
    ]
