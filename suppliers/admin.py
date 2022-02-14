from django.contrib import admin
from suppliers.models import Product, Supplier, Seller, Invoice, Item

# Register your models here.

admin.site.register(Product)
admin.site.register(Supplier)
admin.site.register(Seller)


class InvoiceItemInline(admin.TabularInline):
    model = Item


class InvoiceAdmin(admin.ModelAdmin):
    inlines = [InvoiceItemInline]


admin.site.register(Invoice, InvoiceAdmin)
