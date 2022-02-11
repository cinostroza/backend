from .models import Product, ProductCodes, BsaleCodes
from bsale_api_helper.api_helper import get_variant_list


# TODO 1: Add the functionality to find the products in the invoice in the database,
#  these products must also be associated to a product on Bsale.
#  Steps:
#  Try to find a product using the supplier codes, if this fails, ask the user to associate the product to a Bsale
#  Variant, for this enable the search API similar to the one Bsale offers.

class ProductClass:
    def __init__(self, codes, name, supplier):
        self.codes = codes
        self.name = name
        self.supplier = supplier
        self.price = 0
        self.qty = 0
        self.unit = ""
        self.total_price = 0
        self.bsale_code = None

    def get_product_by_code(self):
        results = []
        for code in self.codes:
            result = get_variant_list(code=code)
            results.append(result['items'])
        print(results)
