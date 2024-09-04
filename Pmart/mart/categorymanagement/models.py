from django.core.exceptions import ValidationError
from django.db import models

from utils.custom_model import CustomModel

# Create your models here.

class ProductCategory(CustomModel):
    name = models.CharField(max_length=255, db_column='name')
    description = models.TextField(blank=True, db_column='description', null=True)
    status = models.BooleanField(db_column='status', default=True)
    parent_category = models.ForeignKey('self', db_column='parentCategory', on_delete=models.SET_NULL, null=True,
                                        blank=True, related_name='parent_categories')

    class Meta:
        db_table = 'ProductCategories'

    def clean(self):
        if not self.name:
            raise ValidationError("Category name is required.")

        if not self.description:
            raise ValidationError("Category description is required.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)