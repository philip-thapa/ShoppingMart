from django.db import models

from categorymanagement.models import ProductCategory
from usermanagement.models import CustomUser
from utils.custom_model import CustomModel, DynamicValidationMixin


# Create your models here.

class Product(DynamicValidationMixin, CustomModel):
    name = models.CharField(max_length=56, db_column='name')
    description = models.TextField(db_column='description', null=True, blank=True)
    price = models.IntegerField(db_column='price')
    category = models.ForeignKey(ProductCategory, db_column='category', related_name='products', null=True, blank=True,
                                 on_delete=models.DO_NOTHING)
    status = models.BooleanField(db_column='status', default='A')
    stock = models.IntegerField(db_column='stock', default=0)
    created_by = models.CharField(db_column='createdBy', max_length=16)

    REQUIRED_FIELDS = ['name', 'price', 'created_by']

    class Meta:
        db_table = 'Products'


class ProductImage(DynamicValidationMixin, CustomModel):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE, db_column='product')
    file_path = models.CharField(db_column="filePath", max_length=256)
    product_image_no = models.BooleanField(default=1, db_column='productImageNo')
    created_by = models.CharField(db_column='createdBy', max_length=16)

    REQUIRED_FIELDS = ['product', 'file_path', 'created_by']

    class Meta:
        db_table = 'ProductImages'
        unique_together = ('product', 'product_image_no')


class Discount(DynamicValidationMixin, CustomModel):
    DISCOUNT_TYPE_CHOICES = [
        ('Percentage', 'Percentage'),
        ('Fixed', 'Fixed'),
    ]

    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, db_column='discountType')
    value = models.DecimalField(max_digits=2, decimal_places=2, db_column='value')
    product = models.ForeignKey(Product, related_name='discounts', on_delete=models.CASCADE, db_column='product',
                                null=True, blank=True)
    category = models.ForeignKey(ProductCategory, related_name='discounts', on_delete=models.CASCADE,
                                 db_column='category', null=True, blank=True)
    start_date = models.DateField(db_column='startDate')
    end_date = models.DateField(db_column='endDate')
    created_by = models.CharField(db_column='createdBy', max_length=16)

    REQUIRED_FIELDS = ['discount_type', 'value', 'product', 'start_date', 'end_date', '']

    class Meta:
        db_table = 'Discounts'


class ProductRating(DynamicValidationMixin, CustomModel):
    product = models.ForeignKey(Product, related_name='ratings', on_delete=models.CASCADE, db_column='product')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='user')
    rating = models.PositiveSmallIntegerField(db_column='rating')  # Rating value between 1 and 5
    review = models.TextField(db_column='review', blank=True, null=True)  # Optional review comment

    REQUIRED_FIELDS = ['product', 'user', 'rating']

    class Meta:
        db_table = 'ProductRatings'
        unique_together = ('product', 'user')

