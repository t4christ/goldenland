# Generated by Django 3.0 on 2022-06-30 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gdapp', '0022_auto_20220625_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='email',
            field=models.EmailField(default='newuser@goldenlandng.com', max_length=255, unique=True, verbose_name='email address'),
        ),
    ]
