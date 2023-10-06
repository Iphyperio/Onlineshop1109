# Generated by Django 4.2.5 on 2023-10-06 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_color_size_product_variant_variants'),
        ('order', '0003_order_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='variant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.variants'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shopcart',
            name='variant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.variants'),
        ),
    ]