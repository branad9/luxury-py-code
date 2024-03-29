# Generated by Django 3.2.15 on 2022-11-08 12:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(blank=True, max_length=250, null=True)),
                ('order_note', models.CharField(blank=True, max_length=250, null=True)),
                ('order_total', models.DecimalField(decimal_places=2, max_digits=20)),
                ('delivery_charges', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('status', models.CharField(choices=[('Ordered', 'Ordered'), ('Shipped', 'Shipped'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Ordered', max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Orders',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderitems', to='orders.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('variation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.productvariation')),
            ],
            options={
                'verbose_name_plural': 'Order Items',
                'ordering': ['-created'],
            },
        ),
    ]
