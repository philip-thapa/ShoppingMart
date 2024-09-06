from django.core.files.base import ContentFile
from django.db.models import Max

from mart.settings import BASE_DIR
from productmanagement.constants import ProductException, ProductImagesPaths, AllowedFormats
from productmanagement.models import Product, ProductImage
from utils.image_handler import ImageHandler
from utils.storage_management import CustomStorage


class ProductCUDManager:

    def __init__(self, request):
        data = request.data
        self.product = Product()
        self.product.name = data.get('name', '').strip()
        self.product.description = data.get('description', '').strip()
        price = data.get('price')
        if not price:
            raise ProductException('Price is required')
        self.product.price = data.get('price')
        category_id = data.get('category')
        if not category_id:
            raise ProductException('Category ID is required')
        self.product.category = category_id
        self.product.stock = data.get('stock', 0)
        self.product.created_by = request.user.email
        self.product.save()
        # handle Image

    def add_new_product(self):
        self.product.save()

    @staticmethod
    def upload_product_image(request):
        data = request.data
        product_id = data.get('productId')
        product_image = data.get('productImage')
        try:
            if ImageHandler.is_image_greater_than_one_mb(product_image):
                raise ProductException("Image size exceeds the 1 MB limit.")
        except Exception as e:
            raise ProductException("Unable to process image")
        compressed_image = ImageHandler.compress_image(product_image)
        path = ProductImagesPaths.PRODUCT_PATH
        location = BASE_DIR + path
        storage = CustomStorage(location)
        file_path = ProductCUDManager.get_saved_product_file_path(product_id, compressed_image, 'product', storage,
                                                     path)
        last_image_no = ProductImage.objects.filter(product_id=product_id).aggregate(Max('product_image_no'))['product_image_no__max']
        if not last_image_no:
            last_image_no = 0
        ProductImage.objects.create(
            product_id=product_id,
            file_path=file_path,
            product_image_no = last_image_no + 1,
            created_by = request.user.email
        )

    @staticmethod
    def get_saved_product_file_path(product_id, file_data, file_type, storage, path):
        content = ContentFile(file_data.read())
        file_extension = file_data.name.split('.')[-1]
        if file_extension.lower() not in AllowedFormats.extensions:
            raise ProductException(
                '{0} is not an allowed format. Please upload {1}'.format(file_extension, ', '.join(
                    AllowedFormats.extensions)))
        file_name = str(product_id) + '_' + file_type + '.' + file_extension
        url = storage.save_file(file_name, content)
        return path + url

