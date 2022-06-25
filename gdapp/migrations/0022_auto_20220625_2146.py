# Generated by Django 3.0 on 2022-06-25 21:46

import cloudinary_storage.storage
import cloudinary_storage.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gdapp', '0021_auto_20220625_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='video',
            field=models.FileField(blank=True, storage=cloudinary_storage.storage.VideoMediaCloudinaryStorage(), upload_to='media/properties/videos', validators=[cloudinary_storage.validators.validate_video]),
        ),
    ]
