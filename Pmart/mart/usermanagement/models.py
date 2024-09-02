import datetime
from time import timezone

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import JSONField
from django.utils import timezone

from django.contrib.auth.models import BaseUserManager


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
