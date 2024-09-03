from django.contrib.auth.backends import ModelBackend
from usermanagement.models import CustomUser
from utils.otp_handler import OTP


class CustomModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None
        try:
            data = request.data
            is_otp = data.get('otp', False)
            email = data.get('email')
            if not is_otp:
                return user
            otp = OTP(dict(email=email))
            if otp.verify(data.get('otp')):
                return CustomUser.objects.get(email=email)
            else:
                raise Exception('Invalid OTP')
        except Exception as e:
            raise Exception('Please try again')
