class ProductException(Exception):
    pass


class ProductImagesPaths:

    PRODUCT_PATH = '/static/files/products/'


class AllowedFormats:
    extensions = ['jpg', 'jpeg', 'pdf', 'png']