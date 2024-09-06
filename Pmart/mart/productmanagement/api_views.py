from rest_framework.response import Response
from rest_framework.views import APIView

from productmanagement.constants import ProductException
from productmanagement.product_cud_manager import ProductCUDManager


# Create your views here.

class AddProduct(APIView):

    def post(self, request):
        try:
            ProductCUDManager(request).add_new_product()
            return Response({'msg': 'success'}, 200)
        except ProductException as e:
            return Response(str(e), 500)
        except Exception as e:
            return Response(str(e), 500)


class UploadProductImage(APIView):

    def post(self, request):
        try:
            ProductCUDManager(request).upload_product_image(request)
            return Response({'msg': 'success'}, 200)
        except ProductException as e:
            return Response(str(e), 500)
        except Exception as e:
            return Response(str(e), 500)
