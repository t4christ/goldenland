# Generated by Django 3.0 on 2022-06-25 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gdapp', '0018_property_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='video',
            field=models.FileField(default='settings.MEDIA_ROOT/properties/media.mp4', upload_to='media/properties/videos'),
        ),
    ]
