import graphene
from graphene_django import DjangoObjectType

from .models import Supplier, Seller, Product


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("name", "bar_code", "cost", "description", "supplier", "item")


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


class CreateSupplier(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        rut = graphene.String()
        address = graphene.String()
        notes = graphene.String()

    ok = graphene.Boolean()
    supplier = graphene.Field(lambda: SupplierType)

    def mutate(root, info, name, rut, address, notes):
        supplier = Supplier(name=name,
                            rut=rut,
                            address=address,
                            notes=notes)
        try:
            supplier.save()
            ok = True
        except Exception:
            ok = False
        return CreateSupplier(supplier=supplier, ok=ok)


class MyMutations(graphene.ObjectType):
    create_supplier = CreateSupplier.Field()


schema = graphene.Schema(query=Query, mutation=MyMutations)
