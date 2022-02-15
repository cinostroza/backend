from django.db import models

"""
Los objetivos de estos modelos son los siguientes:
1.- Asociar automaticamente los codigos de productos de los proveedores con los codigos de los productos en Bsale.
2.- Asociar los productos con proveedores.
3.- Asociar los productos con proveedores y con sus costos netos.
"""


class Supplier(models.Model):
    name = models.CharField(max_length=300, null=False)
    rut = models.CharField(max_length=100, null=False, unique=True)
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
    name = models.CharField(max_length=200, null=False)
    code = models.CharField(max_length=100, null=True, unique=False)
    bsale_code = models.CharField(max_length=50, null=True, unique=False)
    description = models.CharField(max_length=500, null=True)
    suppliers = models.ManyToManyField(Supplier, related_name="products")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ProductCodes(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    code = models.CharField(max_length=200, null=False)


class Invoice(models.Model):
    supplier = models.ForeignKey(Supplier, related_name="invoice", on_delete=models.CASCADE)
    number = models.CharField(max_length=100, name=False)
    date = models.DateField()

    def __str__(self):
        return str(self.number)


class Item(models.Model):
    product = models.ForeignKey(Product, related_name="item", on_delete=models.CASCADE)
    cost = models.FloatField(null=False)
    discount = models.FloatField(null=True)
    units = models.CharField(max_length=20, null=True)
    quantity = models.IntegerField(null=False)
    invoice = models.ForeignKey(Invoice, related_name="item", on_delete=models.CASCADE)

    class Meta:
        ordering = ['product']

    def __str__(self):
        return str(self.product_id)

