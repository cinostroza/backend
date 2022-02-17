import xml.etree.ElementTree as ET
from .product_manager import ProductClass
import pandas
import pathlib
from .models import Supplier, Invoice, Item, Product, ProductCodes, CrudeInvoiceItem


class InvoiceParser:
    def __init__(self, invoice_xml):
        self.code = 0
        self.supplier = ""
        self.supplier_name = ""
        self.product_list = []
        self.invoice_xml = invoice_xml
        self.date = ""
        self.pk = None
        self.parse_invoice()

    def parse_invoice(self):

        tree = ET.parse(self.invoice_xml)
        root = tree.getroot()

        products = [product for product in root.iter("{http://www.sii.cl/SiiDte}Detalle")]
        supplier = [supplier for supplier in root.iter("{http://www.sii.cl/SiiDte}Emisor")]
        supplier_data = {}

        for item in supplier[0].iter():
            for data in item.iter():
                supplier_data[data.tag.replace("{http://www.sii.cl/SiiDte}", "")] = data.text

        self.supplier = supplier_data["RUTEmisor"]
        self.supplier_name = supplier_data["RznSoc"]
        codes = [code for code in root.iter("{http://www.sii.cl/SiiDte}Folio")]
        self.code = codes[0].text
        dates = [date for date in root.iter("{http://www.sii.cl/SiiDte}FchEmis")]
        self.date = dates[0].text
        for product in products:
            product_codes = [code.text for code in product.iter("{http://www.sii.cl/SiiDte}VlrCodigo")]
            product_name = product.find("{http://www.sii.cl/SiiDte}NmbItem").text
            product_qty = float(product.find("{http://www.sii.cl/SiiDte}QtyItem").text)
            product_unit = product.find("{http://www.sii.cl/SiiDte}UnmdItem").text
            product_price = float(product.find("{http://www.sii.cl/SiiDte}PrcItem").text)
            product_total_price = float(product.find("{http://www.sii.cl/SiiDte}MontoItem").text)
            product_supplier = supplier_data["RUTEmisor"]
            try:
                product_discount = float(product.find("{http://www.sii.cl/SiiDte}DescuentoPct").text)
            except Exception:
                product_discount = 0
            current_product = ProductClass(codes=product_codes,
                                           name=product_name,
                                           supplier=product_supplier,
                                           )
            current_product.discount = product_discount
            current_product.price = product_price
            current_product.qty = product_qty
            current_product.unit = product_unit
            current_product.total_price = product_total_price
            current_product.get_product_by_code()
            self.product_list.append(current_product)

    def export_to_excel(self):
        product_dictionary = {}
        names = []
        qtys = []
        prices = []
        total_prices = []
        product_count = 1
        code_len_list = [len(product.codes) for product in self.product_list]
        max_code_len = max(code_len_list)

        for product in self.product_list:

            names.append(product.name)
            qtys.append(product.qty)
            prices.append(product.price)
            total_prices.append(product.total_price)
            code_index = 0

            for i in range(max_code_len):
                try:
                    if product_count == 1:
                        product_dictionary[f"code_{i}"] = product.codes[i]
                    else:
                        product_dictionary[f"code_{i}"] = product_dictionary[f"code_{code_index}"] + \
                                                          " " + product.codes[i]
                except IndexError:
                    if product_count == 1:
                        product_dictionary[f"code_{i}"] = "NaN"
                    else:
                        product_dictionary[f"code_{i}"] = product_dictionary[f"code_{code_index}"] + \
                                                          " " + "NaN"
                code_index += 1
            product_count += 1

        for i in range(max_code_len):
            product_dictionary[f"code_{i}"] = product_dictionary[f"code_{i}"].split()

        product_dictionary["product names"] = names
        product_dictionary["qtys"] = qtys
        product_dictionary["prices"] = prices
        product_dictionary["total_price"] = total_prices
        df = pandas.DataFrame(product_dictionary)
        print(pathlib.Path().resolve())
        df.to_excel(f"./Output/{self.code}.xlsx",
                    encoding="utf-8-sig", index=False)

    def add_supplier_codes(self, supplier):
        for product in self.product_list:
            if product.product is not None:
                supplier.products.add(product.product)
                for code in product.codes:
                    try:
                        code_object = ProductCodes.objects.get(code__exact=code)
                    except ProductCodes.DoesNotExist:
                        code_object = ProductCodes(code=code, supplier=supplier, product=product.product)
                        code_object.save()
        supplier.save()

    def save_invoice(self, supplier):
        try:
            invoice = Invoice.objects.get(number__exact=self.code)
            self.pk = invoice.pk
        except Invoice.DoesNotExist:
            new_invoice = Invoice(supplier=supplier, number=self.code, date=self.date)
            new_invoice.save()
            for product in self.product_list:
                new_crude_item = CrudeInvoiceItem(
                    name=product.name,
                    cost=product.price,
                    discount=product.discount,
                    units=product.unit,
                    quantity=product.qty,
                    invoice=new_invoice
                )
                new_crude_item.save()
            self.pk = new_invoice.pk

    def save(self):

        # This logic needs to check:
        # Are there any products?
        # Is the supplier already on the database? if not add it.
        # Is the product already on the database? if not, add it.
        # is every supplier code on the database? if not, add it.
        # Add each product to the supplier of this invoice.
        # Add all products to crudeInvoiceItems

        if len(self.product_list) == 0:
            # quit if there are no products on the invoice
            return
        else:
            try:
                supplier = Supplier.objects.get(rut__exact=self.supplier)
                self.add_supplier_codes(supplier)
                self.save_invoice(supplier=supplier)
            except Supplier.DoesNotExist:
                new_supplier = Supplier(name=self.supplier_name, rut=self.supplier)
                new_supplier.save()
                self.add_supplier_codes(new_supplier)
                self.save_invoice(supplier=new_supplier)
