from rest_framework import generics
from rest_framework import status
from rest_framework.generics import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import render
from rest_framework.response import Response
from .serializers import *

#create your views here.
class RegistrationApiView(generics.CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data
            }

            return Response(response, status=status_code)

class LoginApiView(generics.CreateAPIView):
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
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'email': serializer.data['email'],
                }
            }

            return Response(response, status=status_code)

class ProfileApiView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_queryset(self):
        try:
            profile = Profile.objects.select_related('user').get(
                user__username=self.kwargs.get('username')
            )
            return profile
        except Exception:

            raise NotFound('profiles not there')

    def retrieve(self, request, **kwargs):
        data = self.get_queryset()
        serializer = self.serializer_class(data, context={'request': request})

        return Response((serializer.data,
                         {"message": 'profile success'}),
                        status=status.HTTP_200_OK)

class UpdateProfileView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.select_related('user').get(
            user__username=self.request.user.username
        )
        return obj

    def patch(self, request, username):
        if request.user.username != username:
            raise PermissionDenied('cannot update profile')
        else:
            data = request.data
            serializer = self.serializer_class(instance=request.user.profiles,
                                               data=data, partial=True)
            serializer.is_valid()
            serializer.save()
            return Response((serializer.data,
                             {"message": 'profile updated'}),
                            status=status.HTTP_200_OK)