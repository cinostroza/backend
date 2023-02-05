from django.contrib import admin
from invoice_manager.models import Product, Supplier, Seller, ProductCodes, Invoice, LineItem

# Register your models here.

admin.site.register(Product)
admin.site.register(Supplier)
admin.site.register(Seller)
admin.site.register(ProductCodes)
admin.site.register(Invoice)
admin.site.register(LineItem)
