# Generated by Django 3.2.15 on 2022-11-21 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_brand_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='meta_desc',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='brand',
            name='meta_keywords',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='brand',
            name='meta_title',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_desc',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_keywords',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_title',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='meta_desc',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='meta_keywords',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='meta_title',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]