from rest_framework import serializers
from .models import VendorProfile, Store, Vendor
from django.contrib.auth.models import User


class VendorProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model =VendorProfile
        fields ='__all__'

        
class StoreSerializer(serializers.ModelSerializer):
    #vendor = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Store
        fields = '__all__'

class VendorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required = True , write_only=True)
    #password2 = serializers.CharField(required = True , write_only=True)
    class Meta:
        model = Vendor
        fields= '__all__'

        def get_isAdmin(self,obj):
         return obj.is_staff
        
    def create(self, validated_data):
        phone_number= validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        email = validated_data.get('email')
        user = User(phone_number=phone_number, email=email)
        user.set_password(password)
        user.save()
        return user
        
class UserSerializerWithToken(VendorSerializer):
    token= serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields= [
            "username",
            "email",
            "password",
            "IsOwner",
            "token",
        ]
