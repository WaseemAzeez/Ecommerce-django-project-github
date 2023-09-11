from django.contrib import admin
from .models import Vendor,VendorProfile, Store
# Register your models here.

admin.site.register(Vendor)
admin.site.register(VendorProfile)
admin.site.register(Store)

