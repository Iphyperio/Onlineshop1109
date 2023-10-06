# Generated by Django 4.2.5 on 2023-10-06 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_color_size_product_variant_variants'),
        ('order', '0004_orderproduct_variant_shopcart_variant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='variant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.variants'),
        ),
        migrations.AlterField(
            model_name='shopcart',
            name='variant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.variants'),
        ),
    ]