import graphene
from graphene_django import DjangoObjectType
from .invoice_parser import InvoiceParser, InvoiceManager
from .models import Supplier, Seller, Product, Invoice, LineItem, ProductCodes
from graphene_file_upload.scalars import Upload
from bsale_api_helper import api_helper


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = '__all__'


class SupplierType(DjangoObjectType):
    class Meta:
        model = Supplier
        fields = ("name", "rut", "address", "notes", "products")


class SellerType(DjangoObjectType):
    class Meta:
        model = Seller
        fields = '__all__'


class InvoiceType(DjangoObjectType):
    class Meta:
        model = Invoice
        fields = '__all__'


class ItemType(DjangoObjectType):
    class Meta:
        model = LineItem
        fields = '__all__'


class AutoCompleteVariantName(graphene.ObjectType):
    name = graphene.String()
    sku = graphene.String()


class ProductCodesType(DjangoObjectType):
    class Meta:
        model = ProductCodes
        fields = ('code', 'bsale_code')


class Query(graphene.ObjectType):
    all_products = graphene.List(ProductType)
    product_by_name = graphene.Field(ProductType, name=graphene.String(required=True))
    product_by_code = graphene.Field(ProductType, code=graphene.String(required=True))
    product_by_partial_name = graphene.List(ProductType, name=graphene.String(required=True))
    all_suppliers = graphene.List(SupplierType)
    supplier_by_name = graphene.Field(SupplierType, name=graphene.String(required=True))
    supplier_by_id = graphene.Field(SupplierType, name=graphene.ID(required=True))
    all_invoices = graphene.List(InvoiceType)
    invoice_by_id = graphene.Field(InvoiceType, id=graphene.ID(required=True))
    invoice_by_supplier = graphene.List(InvoiceType, supplier_rut=graphene.String(required=True))
    autocomplete = graphene.List(AutoCompleteVariantName, q=graphene.String(required=True))

    def resolve_all_products(root, info):
        return Product.objects.filter().all()

    def resolve_product_by_name(root, name):
        try:
            return Product.objects.get(name=name)
        except Product.DoesNotExist:
            return None

    def resolve_product_by_code(root, code):
        try:
            return Product.objects.get(code__exact=code)
        except Product.DoesNotExist:
            return None

    def resolve_product_by_partial_name(root, name):
        try:
            return Product.objects.filter(name__icontains=name).all()
        except Product.DoesNotExist:
            return None

    def resolve_supplier_by_name(root, name):
        try:
            return Supplier.objects.get(name=name)
        except Supplier.DoesNotExist:
            return None

    def resolve_supplier_by_id(root, id):
        try:
            return Supplier.objects.get(id=id)
        except Supplier.DoesNotExist:
            return None

    def resolve_all_suppliers(root, info):
        return Supplier.objects.filter().all()

    def resolve_all_invoices(root, info):
        return Invoice.objects.all()

    def resolve_invoice_by_id(root, info, id):
        try:
            return Invoice.objects.get(id=id)
        except Invoice.DoesNotExist:
            return None

    def resolve_invoice_by_supplier(root, info, rut):
        try:
            return Invoice.objects.filter(supplier__rut__exact=rut).all()
        except Invoice.DoesNotExist:
            return None

    def resolve_autocomplete(self, info, q):
        results = api_helper.get_variant_list(description=q, limit=10)
        if not results:
            return
        response = []
        items = results.get('items', None)
        if not items:
            return
        for item in items:
            response.append(AutoCompleteVariantName(
                name=item.get('description', None),
                sku=item.get('code', None))
            )
        return response


class CreateSupplier(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        rut = graphene.String(required=True)
        address = graphene.String()
        notes = graphene.String()

    ok = graphene.Boolean()
    supplier = graphene.Field(lambda: SupplierType)

    def mutate(root, info, name, rut, **kwargs):
        address = kwargs.get('address')
        notes = kwargs.get('notes')
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


class UpdateSupplierMutation(graphene.Mutation):
    class Meta:
        model = Supplier

    class Arguments:
        name = graphene.String()
        rut = graphene.String()
        address = graphene.String()
        notes = graphene.String()
        id = graphene.ID(required=True)

    supplier = graphene.Field(SupplierType)

    @classmethod
    def mutate(cls, root, info, id, **kwargs):
        supplier = Supplier.objects.get(pk=id)
        if 'name' in kwargs:
            supplier.name = kwargs.get('name')

        if 'rut' in kwargs:
            supplier.rut = kwargs.get("rut")

        if 'address' in kwargs:
            supplier.address = kwargs.get("address")

        if 'notes' in kwargs:
            supplier.notes = kwargs.get("notes")

        supplier.save()
        return UpdateSupplierMutation(supplier=supplier)


class CreateInvoice(graphene.Mutation):
    class Arguments:
        supplier = graphene.String()
        number = graphene.String()
        date = graphene.Date()
        items = graphene.List(graphene.String)

    ok = graphene.Boolean()
    invoice = graphene.Field(lambda: InvoiceType)

    def mutate(root, info, supplier, number, date, items):
        invoice = Invoice(
            supplier=Supplier.objects.filter(rut__exact=supplier).get(),
            number=number,
            date=date
        )
        for item in items:
            new_item = LineItem(
                product=Product.objects.filter(code__exact=item['product']).get(),
                cost=item['cost'],
                discount=item['discount'],
                units=item['items'],
                quantity=item['quantity'],
                invoice=invoice,
            )
            new_item.save()
        ok = True
        return CreateInvoice(invoice=invoice, ok=ok)


class DeleteInvoiceMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    id = graphene.ID()
    ok = graphene.Boolean()

    def mutate(self, info, id, **kwargs):
        try:
            invoice = Invoice.objects.get(id__exact=id)
            invoice.delete()
            ok = True
        except Invoice.DoesNotExist:
            ok = False
        return DeleteInvoiceMutation(id=id, ok=ok)


class UploadMutation(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    success = graphene.Boolean()
    invoice = graphene.Field(InvoiceType)

    def mutate(self, info, file, **kwargs):
        new_invoice = InvoiceParser(file)
        new_invoice.parse_invoice()
        manager = InvoiceManager(new_invoice)
        manager.parse()
        manager.save()
        return UploadMutation(success=True, invoice=manager.invoice_model)


class Mutation(graphene.ObjectType):
    create_supplier = CreateSupplier.Field()
    update_supplier = UpdateSupplierMutation.Field()
    create_invoice = CreateInvoice.Field()
    upload_file = UploadMutation.Field()
    delete_invoice = DeleteInvoiceMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
