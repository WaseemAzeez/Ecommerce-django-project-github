from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
#from django.contrib.auth.models import User
from .models import Profile, User


class ChangePasswordSerializer(serializers.Serializer):
    model=User
    """
    Serializer for password change endpoint
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields='__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required = True , write_only=True)
    password2 = serializers.CharField(required = True , write_only=True)
    class Meta:
        model = User
        fields= [
            "username",
            "email",
            "password",
            "password2",
            "is_staff",
            "is_active",
            "is_superuser"
        ]
        extra_kwargs={
            'password': {'write_only': True},
            'password2': {'write_only': True},

        }
        def get_isAdmin(self,obj):
         return obj.is_staff
        
    def create(self, validated_data):
        username= validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        password2= validated_data.get('password2')
        email = validated_data.get('email')

        if password==password2:
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()
            return user
        else:
            raise serializers.ValidationError({
                'error': 'Both Passwords do not match!'
            })
        
class UserSerializerWithToken(UserSerializer):
    token= serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields= [
            "username",
            "email",
            "password",
            "password2",
            "IsOwner",
            "token",
        ]

    def get_token(self,obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    