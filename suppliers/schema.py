import graphene
from graphene_django import DjangoObjectType

from .models import Supplier, Seller, Product


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("name", "bar_code", "price", "cost", "description", "supplier")


class SupplierType(DjangoObjectType):
    class Meta:
        model = Supplier
        fields = ("name", "rut", "products")


class SellerType(DjangoObjectType):
    class Meta:
        model = Seller
        fields = '__all__'


class Query(graphene.ObjectType):
    all_products = graphene.List(ProductType)
    product_by_name = graphene.Field(ProductType, name=graphene.String(required=True))
    supplier_by_name = graphene.Field(SupplierType, name=graphene.String(required=True))

    def resolve_all_products(root, info):
        return Product.objects.filter().all()

    def resolve_product_by_name(self, root, name):
        try:
            return Product.objects.get(name=name)
        except Product.DoesNotExist:
            return None

    def resolve_supplier_by_name(self, root, name):
        try:
            return Supplier.objects.get(name=name)
        except Supplier.DoesNotExist:
            return None


schema = graphene.Schema(query=Query)
