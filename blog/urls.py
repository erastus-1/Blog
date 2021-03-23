from django.urls import path
from .views import *

urlpatterns = [
    path('api/registration/', RegistrationApiView.as_view(), name='registration'),
    path('api/login/', LoginApiView.as_view(), name='login'),
]