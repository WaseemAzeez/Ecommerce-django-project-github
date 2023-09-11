from django.urls import path
from .views import VendorProfileView,VendorProfileDetailView, VendorProfileCreateView, StoreView, StoreDetailView, StoreCreateView

urlpatterns = [
    path('profile/', VendorProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/', VendorProfileDetailView.as_view(), name='profile-detail'),
    path('profile/create/', VendorProfileCreateView.as_view(), name='profile-create'),
    path('store/', StoreView.as_view(), name='store'),
    path('store/<int:pk>/', StoreDetailView.as_view(), name='store-detail'),
    path('store/create/', StoreCreateView.as_view(), name='store-create'),
]
