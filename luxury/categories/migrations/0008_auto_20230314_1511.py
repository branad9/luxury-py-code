# Generated by Django 3.2.15 on 2023-03-14 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0007_auto_20230107_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='robots',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='schema',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='maincategory',
            name='robots',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='maincategory',
            name='schema',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='robots',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='schema',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_desc',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='maincategory',
            name='meta_desc',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='meta_desc',
            field=models.TextField(blank=True, null=True),
        ),
    ]