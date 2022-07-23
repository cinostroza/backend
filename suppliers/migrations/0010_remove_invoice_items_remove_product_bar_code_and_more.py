# Generated by Django 4.0.6 on 2022-07-23 01:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0009_remove_product_cost_remove_product_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='items',
        ),
        migrations.RemoveField(
            model_name='product',
            name='bar_code',
        ),
        migrations.AddField(
            model_name='invoice',
            name='number',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='invoice',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='item', to='suppliers.invoice'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='bsale_code',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='code',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together={('product', 'invoice')},
        ),
        migrations.CreateModel(
            name='CrudeInvoiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('cost', models.FloatField()),
                ('discount', models.FloatField(null=True)),
                ('units', models.CharField(max_length=20, null=True)),
                ('quantity', models.IntegerField()),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crude_item', to='suppliers.invoice')),
                ('related_item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_item', to='suppliers.item')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]