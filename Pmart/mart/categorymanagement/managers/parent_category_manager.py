from categorymanagement.constants import CategoryException
from categorymanagement.managers.orm_manager import CategoryORMmanager
from categorymanagement.models import ProductCategory


class ParentCategoryManager:

    def __init__(self, request, category_id=None):
        if category_id:
            try:
                self.product_category = CategoryORMmanager.get_category_by_id(category_id)
            except Exception as e:
                raise CategoryException('Invalid category ID')
        else:
            self.__initialize_category_obj__(request.data, request.user)

    def __initialize_category_obj__(self, data, user):
        self.product_category = ProductCategory()
        self.product_category.name = data.get('name', '').strip()
        self.product_category.description = data.get('description', '').strip()
        self.product_category.created_by = user.email

    def add_new_category(self):
        if CategoryORMmanager.check_if_category_exists_by_name(self.product_category.name):
            raise CategoryException("Category name already exists")
        self.product_category.save()


    @staticmethod
    def get_all_categories_details():
        parent_categories_with_children = ProductCategory.objects.filter(parent_category__isnull=True).prefetch_related('parent_categories')
        # return all categories with their child categories details