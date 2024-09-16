from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from usermanagement.api_view import SignUp, SendOTP, MyTokenObtainPairView, GetAllAddress, AddAddress, EditAddress, \
    RemoveAddress, ValidateOTP, SendSignInOtp, SendSignUpOTP, GetUserDetails

urlpatterns = [
    path(r'send-signup-otp', SendSignUpOTP.as_view(), name='send-signup-otp'),
    path(r'sign-up', SignUp.as_view(), name='sign-up'),
    path(r'send-signin-otp', SendSignInOtp.as_view(), name='send-signin-otp'),
    path('sign-in', MyTokenObtainPairView.as_view(), name='sign-in'),
    path(r'send-otp', SendOTP.as_view(), name='send-otp'),
    path(r'verify-otp', ValidateOTP.as_view(), name='verify-otp'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),

    path(r'get-user-details', GetUserDetails.as_view(), name='get-user-details'),

    path('get-all-address', GetAllAddress.as_view(), name='get-all-address'),
    path('add-new-address', AddAddress.as_view(), name='add-new-address'),
    path(r'edit-address', EditAddress.as_view(), name='edit-address'),
    path(r'remove-address', RemoveAddress.as_view(), name='remove-address')
]
