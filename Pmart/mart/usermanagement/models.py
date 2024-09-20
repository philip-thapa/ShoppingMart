from django.contrib.auth.base_user import AbstractBaseUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import JSONField
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager

from datetime import datetime

from usermanagement.constants import ADDRESS_CONSTANTS

from utils.custom_model import CustomModel
from utils.validators import Validators


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('status', 'A')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


# Create your models here.


class CustomUser(AbstractBaseUser):
    gender = (
        ('Male', 'Male'),
        ('Female', 'Female',),
        ('N/A', 'N/A')
    )
    active = (
        ('A', 'A'),
        ('I', 'I')
    )
    email = models.CharField(db_column='Email', max_length=56, unique=True)
    phone = models.CharField(db_column='Phone', max_length=10, blank=True, null=True)
    name = models.CharField(db_column='Name', max_length=16, blank=False, null=False)
    gender = models.CharField(db_column='Gender', max_length=10, blank=True, null=True, choices=gender)
    status = models.CharField(db_column='Status', max_length=1, choices=active, default='A')
    date_of_birth = models.DateField(db_column='DOB', null=True, blank=True)
    loyalty_points = models.IntegerField(db_column='LoyalityPoints', default=0)
    profile_picture = models.ImageField(upload_to='profile_photos/', blank=True, null=True, db_column='Photo')
    is_staff = models.BooleanField(default=False, db_column='IsStaff')
    roles = JSONField(db_column='Roles', default=list)

    created_at = models.DateTimeField(db_column='CreatedAt', default=datetime.now())
    modified_at = models.DateTimeField(db_column='ModifiedAt', default=datetime.now())

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'Users'


class Address(CustomModel):

    user_id = models.ForeignKey(CustomUser, db_column='UserID', on_delete=models.CASCADE, related_name='addresses',
                                null=False, blank=False)
    full_name = models.CharField(max_length=56, db_column='Name', null=False, blank=False)
    phone_number = models.CharField(max_length=10, db_column='Phone', null=False, blank=False)
    pincode = models.CharField(max_length=8, db_column='Pincode', null=False, blank=False)
    state = models.CharField(max_length=56, db_column='State', null=False, blank=False)
    city = models.CharField(max_length=56, db_column='City', null=False, blank=False)
    address = models.TextField(db_column='Address', null=False, blank=False)
    landmark = models.CharField(max_length=256, db_column='Landmark', null=True, blank=True)
    address_type = models.CharField(max_length=8, null=False, db_column='AddressType', blank=False,
                                    default=ADDRESS_CONSTANTS.ADDRESS_TYPES[0])

    class Meta:
        db_table = 'Addresses'

    def clean(self):
        if not self.full_name:
            raise ValidationError("Full name is required.")

        if not self.phone_number:
            raise ValidationError("Phone number is required.")

        elif not Validators.phone_validator(self.phone_number):
            raise ValidationError("Phone number must be of 10 digits")

        if not self.pincode:
            raise ValidationError("Pincode is required.")

        if not self.state:
            raise ValidationError("State is required.")

        if not self.city:
            raise ValidationError("City is required.")

        if not self.address:
            raise ValidationError("Address is required.")

        if not self.address_type or self.address_type not in ADDRESS_CONSTANTS.ADDRESS_TYPES:
            raise ValidationError(f"Address type must be one of the following: "
                                  f"{', '.join(ADDRESS_CONSTANTS.ADDRESS_TYPES)}.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class OtpRequests(CustomModel):
    email = models.CharField(max_length=56, db_column='Email')
    count = models.IntegerField(db_column='Count', default=0)

    class Meta:
        db_table = 'OtpRequests'

