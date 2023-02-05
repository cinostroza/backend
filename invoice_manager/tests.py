from django.test import TestCase

from invoice_manager.models import Supplier


# Create your tests here.

class SupplierTestCase(TestCase):
    def setUp(self) -> None:
        Supplier.objects.create(
            name="foo",
            rut="12345",
            address="123 foo st",
            notes="foobar",
        )

    def test_created_supplier(self):
        supplier = Supplier.objects.get(rut__exact="12345")
        self.assertEqual(supplier.name, "foo")
        self.assertEqual(supplier.notes, "foobar")
        self.assertEqual(supplier.address, "123 foo st")
