from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from accounts.views import (
   # UserRegistrationView,
    UserRegister, 
    UserLogOut,
    UserProfile,
    ProfileDetail,
    ChangePasswordAPIView,
)

urlpatterns = [
    path('login', TokenObtainPairView.as_view(),name='login'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh_view'),
    path('register', UserRegister.as_view(), name='register'),
    #path('registeration/', UserRegistrationView.as_view(), name='registeration'),

    path('profile/', UserProfile.as_view(), name='myprofile'),
    path('profile/<int:id>/', ProfileDetail.as_view(), name='profile-detail'),
    path('logout', UserLogOut.as_view(), name= 'logout_view'),
    path('changepassword', ChangePasswordAPIView.as_view(), name= 'changepassword'),
    #path('reset_password/', include('django_rest_passwordreset.urls', namespace='reset_password')),
    
    path('reset_password/',auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset_password/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(), name='reset_password_complete'),
]
