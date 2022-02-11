from django.db import models


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
    bar_code = models.CharField(max_length=100, null=True, unique=True)
    description = models.CharField(max_length=500, null=True)
    suppliers = models.ManyToManyField(Supplier, related_name="products")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Item(models.Model):
    product = models.ForeignKey(Product, related_name="item", on_delete=models.CASCADE)
    cost = models.FloatField(null=False)
    discount = models.FloatField(null=True)
    units = models.CharField(max_length=20, null=True)
    quantity = models.IntegerField(null=False)

    class Meta:
        ordering = ['product']

    def __str__(self):
        return self.product_id


class Invoice(models.Model):
    supplier = models.ForeignKey(Supplier, related_name="invoice", on_delete=models.CASCADE)
    number = models.CharField(max_length=100, name=False)
    items = models.ManyToManyField(Item, related_name="item")
    date = models.DateField()


class ProductCodes(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    code = models.CharField(max_length=200, null=False)


class BsaleCodes(models.Model):
    product = models.ForeignKey(Product, related_name="bsale_code", on_delete=models.CASCADE)
    code = models.CharField(max_length=50, null=False)
