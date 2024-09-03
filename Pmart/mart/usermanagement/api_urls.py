from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from usermanagement.api_view import SignUp, SendOTP, MyTokenObtainPairView, GetAllAddress, AddAddress, EditAddress, \
    RemoveAddress

urlpatterns = [
    path(r'send-otp', SendOTP.as_view(), name='send-otp'),
    path(r'sign-up', SignUp.as_view(), name='sign-up'),
    path('sign-in', MyTokenObtainPairView.as_view(), name='sign-in'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),

    path('get-all-address', GetAllAddress.as_view(), name='get-all-address'),
    path('add-new-address', AddAddress.as_view(), name='add-new-address'),
    path(r'edit-address', EditAddress.as_view(), name='edit-address'),
    path(r'remove-address', RemoveAddress.as_view(), name='remove-address')
]
