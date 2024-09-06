from categorymanagement.constants import CategoryException
from categorymanagement.models import ProductCategory


class CategoryManager:

    def __init__(self, request):
        data = request.data
        self.child_product_category = ProductCategory()
        self.child_product_category.name = data.get('name', '').strip()
        self.child_product_category.description = data.get('description', '').strip()
        parent_cate_id = data.get('parentCategory')
        if not parent_cate_id:
            raise CategoryException("Invalid parent category ID")
        self.child_product_category.parent_category = parent_cate_id
        self.child_product_category.created_by = request.user.email

    def save_category(self):
        self.child_product_category.save()
