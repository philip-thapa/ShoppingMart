from categorymanagement.models import ProductCategory


class CategoryORMmanager:

    @staticmethod
    def get_category_by_id(category_id):
        return ProductCategory.objects.get(id=category_id)

    @staticmethod
    def check_if_category_exists_by_name(category_name):
        return ProductCategory.objects.filter(name__iexact=category_name).exists()