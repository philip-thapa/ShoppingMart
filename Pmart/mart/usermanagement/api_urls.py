from django.urls import path

from usermanagement.api_view import SignUp

urlpatterns = [
    path(r'sign-up', SignUp.as_view(), name='sign-up'),

]
