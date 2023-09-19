# Generated by Django 4.2.4 on 2023-09-18 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0007_banner'),
        ('order', '0005_remove_orders_product_orders_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='product',
        ),
        migrations.AddField(
            model_name='orders',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='admin_panel.product'),
            preserve_default=False,
        ),
    ]