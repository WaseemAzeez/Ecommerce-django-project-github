from rest_framework import serializers
from .models import Product, Review,AddToCart, Order
from accounts.serializers import UserSerializer
from vendor.serializers import StoreSerializer

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    #user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    vendor = serializers.HiddenField(default=serializers.CurrentUserDefault())
   
    class Meta:
        model = Product
        fields = '__all__'

class AddToCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = AddToCart
        fields ='__all__'

class OrderSerializer(serializers.ModelSerializer):
    shippingAddress = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)  # Changed from User to user
    
    def get_order(self, obj):
        items = Order.objects.filter(order=obj)
        serializer = OrderSerializer(items, many=True)
        return serializer.data
   
    
    def get_user(self, obj):
        serializer = UserSerializer(obj.user)
        return serializer.data
    
    class Meta:
        model = Order
        fields = '__all__'
    
    
    def get_total_price(self, obj):
        return obj.product_item.price * obj.number_in_stock
