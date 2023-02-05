from __future__ import annotations

from typing import List

from django.db import models

from invoice_manager.invoice_parser import ProductType

"""
Los objetivos de estos modelos son los siguientes:
1.- Asociar automaticamente los codigos de productos de los proveedores con los codigos de los productos en Bsale.
2.- Asociar los productos con proveedores.
3.- Asociar los productos con proveedores y con sus costos netos.
"""


class Supplier(models.Model):
    rut = models.CharField(max_length=100, null=False, unique=True)
    name = models.CharField(max_length=300, null=False)
    address = models.CharField(max_length=300, null=True)
    notes = models.CharField(max_length=300, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Seller(models.Model):
    name = models.CharField(max_length=100, null=False)
    email = models.EmailField(null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=False, unique=True)
    description = models.CharField(max_length=500, null=True)
    suppliers = models.ManyToManyField(Supplier, related_name="products")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ProductCodes(models.Model):
    code = models.CharField(max_length=200, null=False, unique=True, primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, related_name='code')
    bsale_code = models.CharField(max_length=200, null=True)


class Invoice(models.Model):
    supplier = models.ForeignKey(Supplier, related_name="invoice", on_delete=models.CASCADE)
    number = models.CharField(max_length=100, name=False)
    date = models.DateField(null=True)

    def __str__(self):
        return str(self.number)


class LineItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name="line_item", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="line_item", on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)
    units = models.CharField(max_length=20, null=True)
    discount = models.FloatField(null=True)
    cost = models.FloatField(null=False)

    class Meta:
        ordering = ['product']
        unique_together = ('product', 'invoice')

    def __str__(self):
        return str(self.product_id)


