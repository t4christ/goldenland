# Generated by Django 3.0 on 2022-06-30 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gdapp', '0027_remove_myuser_is_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='is_staff',
        ),
    ]
