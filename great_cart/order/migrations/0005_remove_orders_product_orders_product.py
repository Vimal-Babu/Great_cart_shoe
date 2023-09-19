# Generated by Django 4.2.4 on 2023-09-18 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0007_banner'),
        ('order', '0004_orders_order_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='product',
        ),
        migrations.AddField(
            model_name='orders',
            name='product',
            field=models.ManyToManyField(to='admin_panel.product'),
        ),
    ]