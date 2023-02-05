import xml.etree.ElementTree as et
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

import pandas
import pathlib

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q

from invoice_manager import models


@dataclass
class ProductType:
    supplier: str = ""
    codes: list = field(default_factory=list)
    name: str = ""
    price: int = 0
    unit: str = ""
    qty: int = 0
    discount: int = 0
    total_price: int = 0


@dataclass
class InvoiceParser:
    """This class can process and invoice in xml format and stores all the relevant data contained in it."""
    invoice_xml: InMemoryUploadedFile
    code: str = ""
    supplier: str = ""
    supplier_name: str = ""
    product_list: List[ProductType] = field(default_factory=list)
    date: str = ""
    pk: str = ""

    def parse_invoice(self):

        tree = et.parse(self.invoice_xml)
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
            current_product = ProductType(codes=product_codes,
                                          name=product_name,
                                          supplier=product_supplier,
                                          )
            current_product.discount = product_discount
            current_product.price = product_price
            current_product.qty = product_qty
            current_product.unit = product_unit
            current_product.total_price = product_total_price
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


@dataclass
class InvoiceManager:
    """This class will turn a ParsedInvoice into a django Invoice Model"""
    parsed_invoice: InvoiceParser
    invoice_model = None

    def parse(self):
        try:
            self.invoice_model = models.Invoice.objects.get(number__exact=self.parsed_invoice.code)
        except models.Invoice.DoesNotExist:
            try:
                supplier = models.Supplier.objects.get(rut__exact=self.parsed_invoice.supplier)
            except models.Supplier.DoesNotExist:
                supplier = models.Supplier.objects.create(
                    name=self.parsed_invoice.supplier_name,
                    rut=self.parsed_invoice.supplier,
                )
            invoice_date = datetime.strptime(self.parsed_invoice.date, '%Y-%m-%d')
            self.invoice_model = models.Invoice.objects.create(
                supplier=supplier,
                number=self.parsed_invoice.code,
                date=invoice_date,
            )

            for product in self.parsed_invoice.product_list:
                try:
                    new_product = models.Product.objects.get(
                        name__exact=product.name
                    )
                except models.Product.DoesNotExist:
                    new_product = models.Product.objects.create(
                        name=product.name,
                        description="",
                    )
                    new_product.suppliers.add(supplier)
                    new_product.save()
                models.LineItem.objects.create(
                    product=new_product,
                    cost=product.price,
                    discount=product.discount,
                    units=product.unit,
                    quantity=product.qty,
                    invoice=self.invoice_model
                )
                for code in product.codes:
                    try:
                        product_code = models.ProductCodes.objects.get(code=code)
                        new_product.code.add(product_code)
                        new_product.save()
                    except models.ProductCodes.DoesNotExist:
                        models.ProductCodes.objects.create(
                            code=code,
                            product=new_product,
                        )

    def save(self):
        self.invoice_model.supplier.save()
        for line_item in self.invoice_model.line_item.all():
            line_item.product.save()
            line_item.save()
        self.invoice_model.save()
