from django.forms import model_to_dict
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from usermanagement.constants import ERROR_MSG, AUTHENTICATION_MSG
from usermanagement.managers.address_manager import AddressManager
from usermanagement.managers.authentication_manager import SignUpManager, OTPManager
from usermanagement.models import CustomUser
from usermanagement.user_exceptions import UserException, OTPException, AddressException
from utils.validators import Validators


@authentication_classes([])
@permission_classes([])
class SendSignUpOTP(APIView):

    def post(self, request):
        try:
            data = request.data
            email = data.get('email').strip()
            if CustomUser.objects.filter(email=email).exists():
                raise UserException(ERROR_MSG.USER_ALREADY_EXIST)
            OTPManager(
                email,
                AUTHENTICATION_MSG.ACTIVATE_ACCOUNT_HEADER,
                AUTHENTICATION_MSG.ACTIVATE_ACCOUNT_BODY).send_otp()
            return Response({'success': True}, 200)
        except UserException as e:
            return Response(str(e), 500)
        except OTPException as e:
            return Response(str(e), 500)
        except Exception as e:
            return Response(str(e), 500, exception=True)


@authentication_classes([])
@permission_classes([])
class SignUp(APIView):

    def post(self, request):
        try:
            data = request.data
            user = SignUpManager(data).signup()
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({
                'success': True,
                'refresh': str(refresh),
                'access': access_token,
            }, 200)
        except UserException as e:
            return Response(str(e), 500)
        except Exception as e:
            return Response(str(e), 500, exception=True)


@authentication_classes([])
@permission_classes([])
class SendSignInOtp(APIView):

    def post(self, request):
        try:
            data = request.data
            email = data.get('email').strip()
            if not CustomUser.objects.filter(email=email).exists():
                raise UserException(ERROR_MSG.USER_DOESNOT_EXIST)
            OTPManager(email, AUTHENTICATION_MSG.SIGN_IN_HEADER, AUTHENTICATION_MSG.SIGN_IN_BODY).send_otp()
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
            return Response({'success': OTPManager(email).validate_otp(otp)}, 200)
        except UserException as e:
            return Response(str(e), 500)
        except OTPException as e:
            return Response(str(e), 500)
        except Exception as e:
            return Response(str(e), 500, exception=True)


class SendOTP(APIView):

    def post(self, request):
        try:
            data = request.data
            # email = data.get('email')
            # header = None
            # msg = None
            # OTPManager(email, header, msg).send_otp()
            return Response({'success': True}, 200)
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
            if not CustomUser.objects.filter(email=attrs.get('email')).exists():
                raise UserException(ERROR_MSG.USER_DOESNOT_EXIST)
            raise UserException(ERROR_MSG.INVALID_CREDENTIALS)


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


class GetUserDetails(APIView):

    def get(self, request):
        try:
            user = request.user
            user_details = {
                'name': user.name,
                'roles': user.roles,
                'email': user.email,
                'is_internal': user.is_staff
            }
            return Response({'success': True, 'user_details': user_details}, 200)
        except Exception as e:
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

