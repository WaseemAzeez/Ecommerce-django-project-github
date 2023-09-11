from django.db import models
from django.contrib.auth.models import User 
#from django.contrib.auth import get_user_model
#User = get_user_model()
from phonenumber_field.modelfields import PhoneNumberField
from vendor.models import Store, Vendor

    
CATEGORY_CHOICES = (
    ('groceries & pets', 'Groceries & Pets'),
    ('health & beauty', 'Health & Beauty'),
    ('mens fashion', 'Mens Fashion'),
    ('Womens fashion', 'Womens Fashion'),
    ('mother & baby', 'Mother & Baby'),
    ('home & lifestyle', 'Home & Lifestyle'),
    ('electronic device', 'Electronic Device'),
    ('electronic accessories', 'Electronic Accessories'),
    ('tv & home appliances', 'TV & Home Appliances'),
    ('sports & outdoor', 'Sports & Outdoor'),
    ('watches, bags & jewellery', 'Watches, Bags & Jewellery'),
    ('automotive & motorbike', 'Automotive & Motorbike'),
)


class Product(models.Model):
    #user= models.ForeignKey(User, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, related_name='store', on_delete=models.CASCADE)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    product_name = models.CharField(max_length=200)
    description = models.TextField()  # Remove the default value
    brand = models.CharField(max_length=200, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='myimages')
    number_in_stock =models.PositiveIntegerField(default=0)  
    is_checked = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
   
    def __str__(self):
        return self.product_name

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='product_review',null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.rating)
    
class AddToCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=1)
   
    def __str__(self):
        return str(self.product)
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_item  = models.ForeignKey(AddToCart,on_delete=models.SET_NULL,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tax_price = models.DecimalField(default=True,max_digits=12, decimal_places=2, null=True, blank=True)
    shipping_price = models.DecimalField(default=True, max_digits=12, decimal_places=2, null=True, blank=True)
    total_price = models.DecimalField(default=True,max_digits=12, decimal_places=2, null=True, blank=True)
    paymentMethod = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    postalCode = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(null=True, blank=True)  
    isDeliver = models.BooleanField(default=False)
    deliveredAt = models.DateTimeField(null=True, blank=True) 
    createdAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.user)
    
class OrderUpdate(models.Model):
    update_id=models.AutoField(primary_key=True)
    order_id= models.IntegerField(default="")
    update_desc=models.CharField(max_length=500)
    timestamp=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:20]+'...'