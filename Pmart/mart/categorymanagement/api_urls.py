from django.urls import path
from categorymanagement.api_views import AddParentCategory, GetAllCategoriesDetails

urlpatterns = [
    # internal
    path(r'add-parent-category', AddParentCategory.as_view(), name='add-parent-category'),
    path(r'get-all-categories-details', GetAllCategoriesDetails.as_view(), name='get-all-categories-details')

    # public

]
