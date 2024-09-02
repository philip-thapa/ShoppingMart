from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from usermanagement.managers.authentication_manager import SignUpManager
from usermanagement.user_exceptions import UserException


@authentication_classes([])
@permission_classes([])
class SignUp(APIView):

    def post(self, request):
        try:
            data = request.data
            SignUpManager(data).signup()
            return Response({'msg': 'success'}, 200)
        except UserException as e:
            return Response(str(e), 400)
        except Exception as e:
            return Response(str(e), 500, exception=True)