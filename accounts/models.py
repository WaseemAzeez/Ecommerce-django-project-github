from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from phonenumber_field.modelfields import PhoneNumberField

#class User(AbstractUser):
#    username= models.CharField(max_length=100)
#    email= models.EmailField(max_length=200)
#    password= models.CharField(max_length=50)
#    password2=models.CharField(max_length=50)

#    def __str__(self):
#        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField(default='') 
    phone_number = models.CharField(max_length=20,null=True, blank=True)
    birthdate = models.DateField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='myimages', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Add more fields as needed for your profile

    def __str__(self):
        return self.user
    
