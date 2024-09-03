from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import JSONField
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager

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


class CustomUser(AbstractUser):
    gender = (
        ('Male', 'Male'),
        ('Female', 'Female',),
        ('N/A', 'N/A')
    )
    active = (
        ('A', 'A'),
        ('I', 'I')
    )
    email = models.CharField(db_column='email',max_length=56, unique=True)
    phone = models.CharField(db_column='phone', max_length=10, blank=True, null=True)
    firstname = models.CharField(db_column='firstName', max_length=16, blank=False, null=False)
    lastname = models.CharField(db_column='lastName', max_length=16, blank=True, null=True)
    gender = models.CharField(db_column='gender', max_length=10, blank=True, null=True, choices=gender)
    status = models.CharField(db_column='status', max_length=1, choices=active, default='A')
    created_at = models.DateTimeField(db_column='createdAt', default=timezone.now)
    modified_at = models.DateTimeField(db_column='modifiedAt', default=timezone.now)
    date_of_birth = models.DateField(db_column='dateOfBirth', null=True, blank=True)
    loyalty_points = models.IntegerField(db_column='loyaltyPoints', default=0)
    profile_picture = models.ImageField(upload_to='profile_photos/', blank=True, null=True, db_column='profilePicture')
    is_staff = models.BooleanField(default=False, db_column='isStaff')
    roles = JSONField(db_column='roles', default=list)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'Users'


class Address(CustomModel):

    user_id = models.ForeignKey(CustomUser, db_column='userId', on_delete=models.CASCADE, related_name='addresses',
                                null=False, blank=False)
    full_name = models.CharField(max_length=56, db_column='fullName', null=False, blank=False)
    phone_number = models.CharField(max_length=10, db_column='phoneNo', null=False, blank=False)
    pincode = models.CharField(max_length=8, db_column='pincode', null=False, blank=False)
    state = models.CharField(max_length=56, db_column='state', null=False, blank=False)
    city = models.CharField(max_length=56, db_column='city', null=False, blank=False)
    address = models.TextField(db_column='address', null=False, blank=False)
    landmark = models.CharField(max_length=256, db_column='landmark', null=True, blank=True)
    address_type = models.CharField(max_length=8, null=False, db_column='addressType', blank=False,
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

