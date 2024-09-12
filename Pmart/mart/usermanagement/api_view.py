from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from usermanagement.constants import ERROR_MSG
from usermanagement.managers.address_manager import AddressManager
from usermanagement.managers.authentication_manager import SignUpManager, OTPManager
from usermanagement.user_exceptions import UserException, OTPException, AddressException
from utils.validators import Validators


@authentication_classes([])
@permission_classes([])
class SignUp(APIView):

    def post(self, request):
        try:
            data = request.data
            SignUpManager(data).signup()
            return Response({'msg': 'success'}, 200)
        except UserException as e:
            return Response(str(e), 500)
        except Exception as e:
            return Response(str(e), 500, exception=True)


@authentication_classes([])
@permission_classes([])
class SendOTP(APIView):

    def post(self, request):
        try:
            data = request.data
            is_sign_in = True if data.get('otp') else False
            OTPManager.send_otp(data.get('email', '').strip(), is_sign_in)
            return Response({'success': True}, 200)
        except UserException as e:
            return Response(str(e), 500)
        except OTPException as e:
            return Response(str(e), 500)
        except Exception as e:
            return Response(str(e), 500, exception=True)


@authentication_classes([])
@permission_classes([])
class ValidateOTP(APIView):

    def post(self, request):
        try:
            data = request.data
            otp = data.get('otp', '').strip()
            email = data.get('email', '').strip()
            return Response({'success': OTPManager.validate_otp(otp, email)}, 200)
        except UserException as e:
            return Response(str(e), 500)
        except OTPException as e:
            return Response(str(e), 500)
        except Exception as e:
            return Response(str(e), 500, exception=True)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        return token

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            data["success"] = True
            return data
        except Exception as e:
            raise UserException('Invalid credentials')


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request,  *args, **kwargs):
        try:
            data = request.data
            if not Validators.email_validator(data.get('email')):
                raise Exception('Invalid Email')
            otp = data.get('otp')
            if otp:
                data['password'] = otp
            response = super(MyTokenObtainPairView, self).post(request,  *args, **kwargs)
            return response
        except Exception as e:
            if request.data.get('otp'):
                return Response(ERROR_MSG.INVALID_OTP, 500)
            return Response(str(e), 500)


class GetAllAddress(APIView):

    def get(self, request):
        try:
            address = AddressManager.get_all_address(request.user)
            return Response({'success': True, 'addresses': address}, 200)
        except Exception as e:
            return Response(str(e), 500)


class AddAddress(APIView):

    def post(self, request):
        try:
            AddressManager().add_new_address(request)
            return Response({'success': True}, 200)
        except AddressException as e:
            return Response(str(e), 500)
        except Exception as e:
            return Response(str(e), 500)


class EditAddress(APIView):

    def post(self, request):
        try:
            address_id = request.data.get('addressId')
            AddressManager(address_id).edit_address(request.data)
            return Response({'success': True}, 200)
        except AddressException as e:
            return Response(str(e), 500)
        except Exception as e:
            return Response(str(e), 500)


class RemoveAddress(APIView):

    def get(self, request):
        try:
            address_id = request.data.get('addressId')
            AddressManager(address_id).remove_address()
            return Response({'success': True}, 200)
        except AddressException as e:
            return Response(str(e), 500)
        except Exception as e:
            return Response(str(e), 500)

