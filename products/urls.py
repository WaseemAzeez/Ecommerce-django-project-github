from django.urls import path
# Import Product Views
from .views import *

urlpatterns = [
    # URLs Path For Product
# Products Urls Path
    path('list/', ProductAPIView.as_view(), name='product-list'),
    path('detail/<int:pk>', ProductDetail.as_view(), name='product-detail'),
    path('create/', ProductCreateView.as_view(), name='product-create'),
    #path('review/', ReviewDetailView.as_view(), name='product-review'),
    path('detail/<int:pk>/review', ReviewDetailView.as_view(), name='productitem-review'),
    path('products/create', ProductCreateView.as_view(), name='product-create'),
    #URLs Path For Orders
    path('cart', AddToCartView.as_view(), name='cart'),
    path('cart/<int:pk>', AddToCartDetailView.as_view(), name='cart-detail'),
    path('order/<int:pk>', OrderItem.as_view(), name='order'),
]   
