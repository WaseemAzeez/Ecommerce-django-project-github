from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from accounts.serializers import UserSerializer,UserSerializerWithToken, ProfileSerializer, ChangePasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile
from rest_framework.generics import UpdateAPIView
from .permissions import IsOwner
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, RetrieveAPIView
from accounts.models import User  
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter


class ChangePasswordAPIView(UpdateAPIView):
    """
        An Endpoint for changing password.
    """
    template_name='accounts/change_password.html'
    serializer_class= ChangePasswordSerializer
    permission_classes= [IsAuthenticated, IsOwner]

    def get_object(self, queryset=None):
        obj=  self.request.user
        return obj
    
    def update(self,request, *args, **kwargs):
        self.object =self.get_object()
        serializer =self.get_serializer(data =request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)  # To update session after password change
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserRegister(APIView):
    serializer_class = UserSerializer
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            user_data ={
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user':serializer.data,
            }
            return Response(user_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogOut(APIView):
    template_name='user_logout.html'
    def post(self, request, format=None):
        try:
            refresh_token = request.data.get('refresh_token')
            token_obj = RefreshToken(refresh_token)
            token_obj.blacklist()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserProfile(APIView):
    template_name= 'user_profile'
    serializer_class = ProfileSerializer
    queryset= User.objects.all()
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active', 'user']
    ordering_fields=('is_active', 'username')

    #def get_queryset(self):
    #    return Profile.objects.filter(user=self.request.user)

    def get(self, request, format=None):
        profile = Profile.objects.all()
        serializer = ProfileSerializer(profile, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProfileDetail(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update, Destroy a profile
    """
    template_name = 'profile_detail.html'
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            raise Http404("Profile does not exist for this user.")

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)