# Generated by Django 4.0.6 on 2023-02-03 23:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=300)),
                ('address', models.CharField(max_length=300, null=True)),
                ('notes', models.CharField(max_length=300, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice_manager.supplier')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ProductCodes',
            fields=[
                ('code', models.CharField(max_length=200, primary_key=True, serialize=False, unique=True)),
                ('bsale_code', models.CharField(max_length=200, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='code', to='invoice_manager.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='invoice_manager',
            field=models.ManyToManyField(related_name='products', to='invoice_manager.supplier'),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=100)),
                ('date', models.DateField(null=True)),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice', to='invoice_manager.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='LineItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('units', models.CharField(max_length=20, null=True)),
                ('discount', models.FloatField(null=True)),
                ('cost', models.FloatField()),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='line_item', to='invoice_manager.invoice')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='line_item', to='invoice_manager.product')),
            ],
            options={
                'ordering': ['product'],
                'unique_together': {('product', 'invoice')},
            },
        ),
    ]
