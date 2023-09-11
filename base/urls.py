from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from .views import HomeAPIView , AboutAPIView, ContactAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', HomeAPIView.as_view(), name='Home'),
    path('about/', AboutAPIView.as_view(), name='About'),
    path('contact/', ContactAPIView.as_view(), name='Contact'),
    path('accounts/', include('accounts.urls')),
    path('vendor/', include('vendor.urls')),
    path('products/', include('products.urls')),
    path('chat/', include('chat.urls')),

    path('openapi', get_schema_view(
        title="E-Commerce app",
        description="API for all things …",
        version="1.0.0"
    ), name='openapi-schema'),

    path('', TemplateView.as_view(
        template_name='swager.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='api_swager'),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
