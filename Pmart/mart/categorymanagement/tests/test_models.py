from django.test import TestCase
from django.core.exceptions import ValidationError

from categorymanagement.models import ProductCategory


class ProductCategoryModelTest(TestCase):

    def setUp(self):
        # Set up a valid parent category
        self.parent_category = ProductCategory.objects.create(
            name="Electronics",
            description="Category for all electronic items",
            status=True
        )

    def test_create_valid_category(self):
        category = ProductCategory(
            name="Mobile Phones",
            description="Category for mobile phones",
            status=True,
            parent_category=self.parent_category
        )
        category.save()
        self.assertEqual(ProductCategory.objects.count(), 2)  # Including the parent category

    def test_create_category_without_name(self):
        category = ProductCategory(
            name="",
            description="Category without name",
            status=True,
            parent_category=self.parent_category
        )
        with self.assertRaises(ValidationError) as context:
            category.save()
        self.assertEqual(str(context.exception), "['Category name is required.']")

    def test_create_category_without_description(self):
        category = ProductCategory(
            name="Headphones",
            description="",
            status=True,
            parent_category=self.parent_category
        )
        with self.assertRaises(ValidationError) as context:
            category.save()
        self.assertEqual(str(context.exception), "['Category description is required.']")

    def test_create_category_without_parent(self):
        category = ProductCategory(
            name="Accessories",
            description="Category for accessories",
            status=True
        )
        category.save()
        self.assertIsNone(category.parent_category)

    def test_create_category_with_inactive_status(self):
        category = ProductCategory(
            name="Cameras",
            description="Category for cameras",
            status=False,
            parent_category=self.parent_category
        )
        category.save()
        self.assertFalse(category.status)