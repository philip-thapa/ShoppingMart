from django.db import IntegrityError

from usermanagement.constants import GenderConstants, AUTHENTICATION_MSG
from usermanagement.models import CustomUser
from usermanagement.user_exceptions import UserException, OTPException
from utils.mail_handler import MailHandler
from utils.otp_handler import OTP
from utils.validators import Validators


class SignUpManager:

    def __init__(self, payload):
        self.email = payload.get('email', '').strip()
        self.password = payload.get('password', '').strip()
        self.phone = payload.get('phone', '').strip()
        self.gender = payload.get('gender', '').strip()
        self.firstname = payload.get('firstName', '').strip()
        self.lastname = payload.get('lastName', '').strip()
        self.otp = payload.get('otp', '').strip()

    def validate_payload(self):
        if len(self.password) < 5:
            raise UserException('Password too short. Minimum 5 char is required')
        if not Validators.email_validator(self.email):
            raise UserException('Invalid Email format')
        if not self.otp:
            raise UserException('Otp is required')
        if self.phone and not Validators.phone_validator(self.phone):
            raise UserException('Invalid phone number')
        if self.gender and self.gender not in GenderConstants.ALL:
            raise UserException('Invalid gender type')
        if not self.firstname:
            raise UserException('First name is required')

    def signup(self):
        self.validate_payload()
        if not OTPManager.validate_otp(self.otp, self.email):
            raise OTPException('Invalid OTP')
        try:
            CustomUser.objects.create_user(
                email=self.email,
                password=self.password,
                phone=self.phone,
                firstname=self.firstname,
                lastname=self.lastname,
            )
            return
        except IntegrityError as e:
            raise UserException('User account already exists')


class OTPManager:

    @staticmethod
    def send_otp(email, is_sign_in=False):
        if not email:
            raise UserException('Email is required')
        if not Validators.email_validator(email):
            raise UserException('Invalid Email')

        if not is_sign_in:
            existing_users = CustomUser.objects.filter(email=email)
            if existing_users:
                raise UserException('User already exists')

        otp = OTP(dict(email=email))
        code = otp.generate_otp()
        if code:
            if is_sign_in:
                MailHandler.send_custom_mail(
                    AUTHENTICATION_MSG.SIGN_IN_HEADER,
                    AUTHENTICATION_MSG.SIGN_IN_BODY + '  ' + str(code),
                    email
                )
            else:
                MailHandler.send_custom_mail(
                    AUTHENTICATION_MSG.ACTIVATE_ACCOUNT_HEADER,
                    AUTHENTICATION_MSG.ACTIVATE_ACCOUNT_BODY + '  ' + str(code),
                    email
                )
        else:
            raise OTPException('Failed to send OTP. Please try again')

    @staticmethod
    def validate_otp(otp, email):
        if not otp or not email:
            raise UserException('Otp and email are required')

        otp_obj = OTP(dict(email=email))
        is_verified = otp_obj.verify(otp)

        if is_verified:
            return True
        return False
