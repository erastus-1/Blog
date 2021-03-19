from django.urls import path
from .views import *

urlpatterns = [
    path('Api/registration/', RegistrationApiView.as_view(), name='registration'),
    path('Api/login/', LoginView.as_view(), name='login'),
]