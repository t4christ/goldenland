# Generated by Django 3.0 on 2022-05-01 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gdapp', '0015_auto_20220501_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realtor',
            name='referral',
            field=models.CharField(default='', max_length=50),
        ),
    ]
