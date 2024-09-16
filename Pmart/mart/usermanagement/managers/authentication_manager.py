from django.db import IntegrityError, transaction
from django.utils.datetime_safe import datetime

from usermanagement.constants import GenderConstants
from usermanagement.models import CustomUser, OtpRequests
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
        if not OTPManager(self.email).validate_otp(self.otp):
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

    def __init__(self, email, header=None, message=None):
        if not email.strip():
            raise UserException('Invalid Email')
        if not Validators.email_validator(email):
            raise UserException('Invalid Email format')
        self.email = email.strip()
        self.header = header
        self.message = message
        self.code = None

    def send_otp(self):
        with transaction.atomic(using='default'):
            otp_request = self.get_or_create_otp_request()
            if otp_request.count >= 20:
                raise OTPException('Otp limit exceeded')
            otp = OTP(dict(email=self.email))
            self.code = otp.generate_otp()
            if self.code:
                MailHandler.send_custom_mail(
                    self.header,
                    self.message + '  ' + str(self.code),
                    self.email
                )
            else:
                raise OTPException('Failed to send OTP. Please try again')
            otp_request.count += 1
            otp_request.save()

    def validate_otp(self, otp):
        if not otp:
            raise UserException('Otp is required')
        self.code = otp

        otp_obj = OTP(dict(email=self.email))
        is_verified = otp_obj.verify(self.code)

        if is_verified:
            return True
        return False

    def get_or_create_otp_request(self):
        today = datetime.now()
        return OtpRequests.objects.get_or_create(email=self.email, createdAt__date=today)[0]
