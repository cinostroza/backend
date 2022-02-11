# Generated by Django 4.0.1 on 2022-01-26 21:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0002_product_cost_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='supplier',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='suppliers.supplier'),
            preserve_default=False,
        ),
    ]
