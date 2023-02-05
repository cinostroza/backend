import requests

BSALE_API_ADDRESS = "https://api.bsale.cl/"
API_TOKEN = "7a2bffa2db0f3cfd1054e8e187a7af33df39f974"
GET_PRODUCT_LIST = "/v1/products.json"
GET_PRODUCT_QUANTITY = "/v1/products/count.json"
GET_VARIANT_LIST = "/v1/variants.json"
HEADERS = {
    'access_token': API_TOKEN
}


def get_product_list(**kwargs):
    """
    This function will query for products o the BSALE APP.

    :param kwargs:
        limit, limita la cantidad de items de una respuesta JSON, por defecto el limit es 25, el máximo permitido es 50.

        offset, permite paginar los items de una respuesta JSON, por defecto el offset es 0.

        fields, solo devolver atributos específicos de un recurso

        expand, permite expandir instancias y colecciones.

        name, Permite filtrar por nombre del producto.

        ledgeraccount, filtra por cuenta contable de los productos.

        costcenter, filtra centro de costo de los productos.

        producttypeid, filtra por tipo de producto.

        state, boolean (0 o 1) indica si los productos están activos(0) inactivos (1).
    :return: Json data
    """

    params = {
        'limit': kwargs.get('limit'),
        'offset': kwargs.get('offset'),
        'fields': kwargs.get('fields'),
        'expand': kwargs.get('expand'),
        'name': kwargs.get('name'),
        'ledgeraccount': kwargs.get('ledgeraccount'),
        'costcenter': kwargs.get('costcenter'),
        'producttypeid': kwargs.get('producttypeid'),
        'state': kwargs.get('state')
    }

    result = requests.get(url=BSALE_API_ADDRESS + GET_PRODUCT_LIST, params=params, headers=HEADERS)
    result.raise_for_status()
    return result.json()


def get_product_quantity(**kwargs):
    """Returns the total quantity of products registered
    state: 0 Active, 1: Inactive"""

    params = {
        'state': kwargs.get('state'),
    }

    result = requests.get(url=BSALE_API_ADDRESS + GET_PRODUCT_QUANTITY, params=params, headers=HEADERS)
    result.raise_for_status()
    return result.json()


def get_variant_list(**kwargs):
    """

    :param kwargs:
    limit, limita la cantidad de items de una respuesta JSON, por defecto el limit es 25, el máximo permitido es 50.

    offset, permite paginar los items de una respuesta JSON, por defecto el offset es 0.

    fields, solo devolver atributos específicos de un recurso

    expand, permite expandir instancias y colecciones.

    description, Permite filtrar por nombre de la variante.

    barcode, filtra por código de barra de la variante.

    code, filtra por código (SKU) de la variante.

    serialnumber, filtra por numero de serie de la variante.

    productid, filtra variantes por el id del producto.

    state, boolean (0 o 1) indica si las variantes están activas(0) o inactivas (1).
    :return: Json data
    """

    params = {
        'limit': kwargs.get('limit'),
        'offset': kwargs.get('offset'),
        'fields': kwargs.get('fields'),
        'expand': kwargs.get('expand'),
        'description': kwargs.get('description'),
        'barcode': kwargs.get('barcode'),
        'code': kwargs.get('code'),
        'serialnumber': kwargs.get('serialnumber'),
        'productid': kwargs.get('productid')
    }
    result = requests.get(url=BSALE_API_ADDRESS + GET_VARIANT_LIST, params=params, headers=HEADERS)
    result.raise_for_status()
    return result.json()


def get_product(url):
    """
    This endpoint returns data for a specific product.
    :param url: Complete url for the product endpoint.
    :return: Json data
    """
    result = requests.get(url=url, headers=HEADERS)
    result.raise_for_status()
    return result.json()


def get_url(url):
    """
    This function will get the data from any endpoint that's harc oded into a full url.
    :param: This function only takes the full url for an endpoint, no params.
    :return: Json data
    """
    result = requests.get(url=url, headers=HEADERS)
    result.raise_for_status()
    return result.json()

