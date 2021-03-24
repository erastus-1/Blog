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


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Profile
        fields = ('username','email','first_name','last_name','image','contact','bio','gender')
        read_only_fields = ('created_date', 'modified_date', 'username')


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('first_name','last_name','image','contact','bio','gender')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'contact': {'required': True},
            'image': {'required': True},
            'bio': {'required': True},
            'gender': {'required': True},
        }
        read_only_fields = ('created_date', 'modified_date')

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.bio = validated_data['bio']
        instance.image = validated_data['image']
        instance.gender = validated_data['gender']
        instance.contact = validated_data['contact']

        instance.save()
        return instance
