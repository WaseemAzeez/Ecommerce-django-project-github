from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Vendor

User = get_user_model()

from django.db.models.signals import pre_save
from django.contrib.auth.models import User


def VendorProfile(sender,instance,**kwargs):
    user = instance
    if user.phone_number != '':
        user.username = user.phone_number
pre_save.connect(VendorProfile,sender = User)

@receiver(post_save, sender=User)
def create_vendor_profile(sender, instance, created, **kwargs):
    if created:
        Vendor.objects.create(user=instance, name='Store Name')

User.profile = property(lambda u: Vendor.objects.get_or_create(user=u)[0])