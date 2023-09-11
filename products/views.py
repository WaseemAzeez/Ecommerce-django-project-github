from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status
from decimal import Decimal
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.renderers import JSONRenderer
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from django_filters import FilterSet
from django_filters import rest_framework as filters
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView, ListCreateAPIView
from .models import (
    Product,
    AddToCart,
    Order,
    Review
)
from .permissions import IsOwner
from .serializers import (
    ProductSerializer,
    AddToCartSerializer,
    OrderSerializer,
    ReviewSerializer
)

class ProductFilter(FilterSet):
    product_name=filters.CharFilter('product_name')
    category=filters.CharFilter('category')
    
    class Meta:
        model=Product
        fields=('product_name', 'category')
    


# Product Item views
class ProductAPIView(ListCreateAPIView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    serializer_class = ProductSerializer
    queryset= Product.objects.all()
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class= ProductFilter
    search_fields = ('product_name', 'description')  # Define fields for searching
    ordering_fields = ('product_name', 'price')

    def get_queryset(self):
        search_query = self.request.GET.get('search')
        queryset = super().get_queryset()
        
        if search_query:
            queryset = queryset.filter(product_name__icontains=search_query)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context
    
    def get(self, request, format=None):
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProductDetail(RetrieveUpdateDestroyAPIView):
    #template_name='product_detail.html'
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    #renderer_classes =[JSONRenderer]
    permission_classes = [IsAuthenticated]

class ProductCreateView(CreateAPIView):
    template_name='product_create.html'
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsOwner]

class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    template_name='review.html'
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        user = request.user
        product = Product.objects.get(id=pk)
        data = request.data
        already_exists = product.review_set.filter(user=user).exists()

        if already_exists:
            content = {'detail': 'Product already reviewed'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        elif data['rating'] == 0:
            content = {'detail': 'Please Select a rating'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            review = Review.objects.create(
                user=user,
                product=product,
                name=user.first_name,
                rating=data['rating'],
                comment=data['comment'],
            )

            reviews = product.review_set.all()
            product.numReviews = len(reviews)

            total = sum(i.rating for i in reviews)
            product.rating = total / len(reviews)
            product.save()

            return Response('Review Added')
 
# Order views
class AddToCartView(ListAPIView):
    template_name='add_to_cart.html'
    queryset = AddToCart.objects.all()
    serializer_class = AddToCartSerializer
    permission_classes=[IsOwner, IsAuthenticated]

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        cart = AddToCart.objects.filter(user=request.user)
        serializer = AddToCartSerializer(cart, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AddToCartDetailView(RetrieveUpdateDestroyAPIView):
    template_name='add_to_cart_detail.html'
    queryset = AddToCart.objects.all()
    serializer_class = AddToCartSerializer
    permission_classes = [IsAuthenticated, IsOwner]

class OrderItem(APIView):
    template_name='order_summary.html'
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = OrderSerializer  # Update with your OrderSerializer
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, format=None):
        try:
            product = Product.objects.get(id=pk)
            quantity = int(request.GET.get('quantity', 2)) # Get quantity from the request query parameters

            shipping_price = Decimal(10)
            tax_price = Decimal(20)
            product_price = product.price * quantity  # Calculate product price based on quantity
            total_price = product_price + shipping_price + tax_price

            cart_obj, created = AddToCart.objects.get_or_create(user=request.user, product=product)
            quantity = cart_obj.quantity
            Order.objects.create(
                user=request.user,
                order_item=cart_obj,
                price=product_price,
                tax_price=tax_price,
                shipping_price=shipping_price,
                total_price=total_price)
            return HttpResponse('Order added successfully!')
        except Product.DoesNotExist:
            return HttpResponse('Product not found!', status=status.HTTP_404_NOT_FOUND)