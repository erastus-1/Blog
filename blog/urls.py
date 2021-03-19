from django.urls import path
from .views import *

urlpatterns = [
    path('registration/', RegistrationApiView.as_view(), name='registration'),
    path('login/', LoginApiView.as_view(), name='login'),
]