from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from categorymanagement.constants import CategoryException
from categorymanagement.managers.parent_category_manager import ParentCategoryManager


# Create your views here.

class AddParentCategory(APIView):

    def post(self, request):
        try:
            ParentCategoryManager(request).add_new_category()
            return Response({'msg': 'success'}, 200)
        except CategoryException as e:
            return Response(str(e), 500)
        except Exception as e:
            return Response(str(e), 500)


class GetAllCategoriesDetails(APIView):

    def post(self, request):
        try:
            ParentCategoryManager.get_all_categories_details()
            return Response({'msg': 'success'}, 200)
        except CategoryException as e:
            return Response(str(e), 500)
        except Exception as e:
            return Response(str(e), 500)