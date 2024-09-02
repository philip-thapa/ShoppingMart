from django.db import IntegrityError

from usermanagement.constants import GenderConstants
from usermanagement.models import CustomUser
from usermanagement.user_exceptions import UserException
from utils.validators import Validators


class SignUpManager:

    def __init__(self, payload):
        self.email = payload['email'].strip()
        self.password = payload['password'].strip()
        self.phone = payload.get('phone', '').strip()
        self.gender = payload.get('gender', '').strip()
        self.firstname = payload.get('firstName', '').strip()
        self.lastname = payload.get('lastName', '').strip()

    def validate_payload(self):
        if len(self.password) < 5:
            raise UserException('Password too short. Minimum 5 char is required')
        if not Validators.email_validator(self.email):
            raise UserException('Invalid Email format')
        if self.phone and not Validators.phone_validator(self.phone):
            raise UserException('Invalid phone number')
        if self.gender and self.gender not in GenderConstants.ALL:
            raise UserException('Invalid gender type')
        if not self.firstname:
            raise UserException('First name is required')

    def signup(self):
        SignUpManager.validate_payload(self)
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

