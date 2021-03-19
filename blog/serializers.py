from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from .models import User


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

    email = serializers.EmailField( required=True,
        allow_null=False,
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
    
    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        email = data['email']
        password = data['password']
        user = authenticate(email=email, password=password)
        user.save()

        return data
