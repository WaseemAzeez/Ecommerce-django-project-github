from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
#from django_filters import rest_framework as filters
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import VendorProfile, Store
from .serializers import VendorProfileSerializer, StoreSerializer
from .permissions import IsOwner

# Create your views here.
# Vendor Views
class VendorProfileView(ListAPIView):
    template_name='vendor_profile.html'
    queryset= VendorProfile.objects.all()
    serializer_class = VendorProfileSerializer
    permission_classes= [IsAuthenticated, IsOwner]
    renderer_classes = [JSONRenderer]
#    renderer_classes = [JSONRenderer]
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        vendors = VendorProfile.objects.filter(user=request.user)
        serializer = VendorProfileSerializer(vendors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class VendorProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset = VendorProfile.objects.all()
    serializer_class = VendorProfileSerializer
    permission_classes = [IsAuthenticated, IsOwner]

class VendorProfileCreateView(CreateAPIView):
    serializer_class = VendorProfileSerializer
    permission_classes = [IsAuthenticated, IsOwner]

class StoreView(ListAPIView):
    template_name='store_list.html'
    queryset= Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes= [IsAuthenticated, IsOwner]
#    renderer_classes = [JSONRenderer]
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        stores = Store.objects.filter(user=request.user)
        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class StoreDetailView(RetrieveUpdateDestroyAPIView):
    template_name='store_detail.html'
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated, IsOwner]

class StoreCreateView(CreateAPIView):
    template_name='store_create.html'
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated,IsOwner]