from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify
from django.utils import timezone
from .managers import UserManager
from django.contrib.auth.models import AbstractUser
from .validators import validate_bvn, validate_tin
# Create your models here.


def business_files(instance, filename):
    slug_name = slugify(instance.email)
    return f'document_image/{slug_name}/{filename}'


def upload_to(instance, filename):
    slug_name = slugify(instance.email)
    return f'pfp/{slug_name}/{filename}'
    

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, blank=False, null=True)
    phone = PhoneNumberField(blank=False, null=True, unique=True)
    pfp = models.ImageField(upload_to=upload_to, blank=False, null=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=6,choices=[
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ], 
    default='Male')

    # Kyc Verification
    address = models.TextField(null=True, blank=False)
    document_type = models.CharField(max_length=30,choices=[
            ("NIN", "National ID Card / NIN Slip"),
            ("PASSPORT", "International Passport"),
            ("PHOTO", "Passport Photograph"),
            ("DL", "Driver's License"),
            ("PVC", "Permanent Voter's Card"),
            ("UTILITY", "Utility Bill"),
    ], blank=False, null=True, default='NIN')
    document_image = models.ImageField(upload_to=business_files, blank=False, null=True)
    bvn_number = models.CharField(null=True, blank=False, unique=True, max_length=11, validators=[validate_bvn], help_text="Bank Verification Number")
    tin_number = models.CharField(null=True, blank=False, unique=True, max_length=12, validators=[validate_tin], help_text="TAX Identification Number")
    is_verified = models.BooleanField(default=False)

    # Django core
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    objects = UserManager()

    def __str__(self):
        return self.email