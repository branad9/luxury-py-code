# Generated by Django 3.2.15 on 2023-03-29 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='image_thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='images/gallery_thumbnails'),
        ),
    ]
