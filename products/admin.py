from django.contrib import admin
from .models import Product, Review, AddToCart, Order, OrderUpdate

# Register your models here.
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(AddToCart)
admin.site.register(Order)
admin.site.register(OrderUpdate)

