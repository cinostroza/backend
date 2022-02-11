from django.contrib import admin
from suppliers.models import Product, Supplier, Seller
# Register your models here.

admin.site.register(Product)
admin.site.register(Supplier)
admin.site.register(Seller)

