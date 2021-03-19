from django.urls import path
from .views import *

urlpatterns = [
    path('', RegistrationApiView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
]