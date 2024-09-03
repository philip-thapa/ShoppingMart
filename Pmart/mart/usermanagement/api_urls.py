from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from usermanagement.api_view import SignUp, SendOTP, MyTokenObtainPairView

urlpatterns = [
    path(r'send-otp', SendOTP.as_view(), name='send-otp'),
    path(r'sign-up', SignUp.as_view(), name='sign-up'),
    path('sign-in', MyTokenObtainPairView.as_view(), name='sign-in'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
