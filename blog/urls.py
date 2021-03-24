from django.urls import path
from .views import *

urlpatterns = [
    path('api/registration/', RegistrationApiView.as_view(), name='registration'),
    path('api/login/', LoginApiView.as_view(), name='login'),
    path('api/profiles/<str:username>/', ProfileApiView.as_view(), name='profile'),
    path('api/profiles/<str:username>/update/', UpdateProfileView.as_view(), name='update_profile'),
]