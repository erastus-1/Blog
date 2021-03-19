from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import *


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        allow_null=False,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message= "Email already exist.",
            )
        ],
        error_messages={
            'required': "This field is required.",
        }
    )

    password = serializers.RegexField(
        regex=("^(?=.{8,}$)(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*"),
        max_length=30,
        required=True,
        allow_null=False,
        write_only=True,
        error_messages={
            'required': "This field is required.",
            'max_length': 'Password cannot be more than 30 characters',
        }
        )

    username = serializers.RegexField(
        regex='^(?!.*\ )[A-Za-z\d\-\_]+$',
        allow_null=False,
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message= "Username already exist.",
            )
        ],
        error_messages={
            'required': "This field is required.",
            'invalid': "Username cannot have spaces or special characters."
        }
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'id', 'password']

    @classmethod
    def create(self, data):
        return User.objects.create_user(**data)


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        email = data['email']
        password = data['password']
        user = authenticate(email=email, password=password)
        user.save()

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")
        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)
            update_last_login(None, user)
            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'email': user.email,
            }
            return validation
            
        except AuthUser.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")
