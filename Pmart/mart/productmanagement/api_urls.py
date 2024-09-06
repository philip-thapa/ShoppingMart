from django.urls import path

from productmanagement.api_views import AddProduct, UploadProductImage

urlpatterns = [
    path(r'add-new-product', AddProduct.as_view(), name='add-new-product'),
    path(r'upload-product-image', UploadProductImage.as_view(), name='upload-product-image')
]