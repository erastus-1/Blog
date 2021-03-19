from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import render
from rest_framework.response import Response
from .serializers import *

#create your views here.

class RegistrationApiView(generics.CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = RegistrationSerializer

    def post(self, request):
        user_data = request.data

        serializer = self.serializer_class(data=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED

        return_message = {
            "success": True,
            "statusCode": status_code,
            "message": "User successfully registered!",
            "data": serializer.data
        }

        return Response(return_message, status=status.HTTP_201_CREATED)

class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'You are successfully Loggedin',
                'authUser': {
                    'email': serializer.data['email'],
                }
            }

            return Response(response, status=status_code)