# Generated by Django 4.0.1 on 2022-02-01 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0007_rename_supplier_product_suppliers_supplier_address_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='seller',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='supplier',
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.FloatField()),
                ('discount', models.FloatField(null=True)),
                ('units', models.CharField(max_length=20, null=True)),
                ('quantity', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item', to='suppliers.product')),
            ],
            options={
                'ordering': ['product'],
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('items', models.ManyToManyField(related_name='item', to='suppliers.Item')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice', to='suppliers.supplier')),
            ],
        ),
    ]
