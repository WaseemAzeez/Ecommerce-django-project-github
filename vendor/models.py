from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
#from django.contrib.auth.models import AbstractUser

class Vendor(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number= models.CharField(max_length=100, unique=True)
    email=models.EmailField(max_length=100, default=True)
    is_phone_verified=models.BooleanField()
    email=models.EmailField(max_length=100, default=True)
    is_email_verified=models.BooleanField()
    password=models.CharField(max_length=20)

    def __str__(self):
        return self.phone_number

class VendorProfile(models.Model):
    vendor= models.OneToOneField(Vendor, related_name='vendor', on_delete=models.CASCADE)
    name= models.CharField(max_length=200)
    bio = models.TextField(max_length=500, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(default='') 
    phone_number = PhoneNumberField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='myimages', blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Store(models.Model):
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    description = models.TextField()
    is_deleted = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name

