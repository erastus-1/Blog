from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import *
from django.db.models.signals import post_save


# Create your models here.
class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User` for free.
    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, username, email, password=None):
        """Create and return a `User` with an email, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """
        Create and return a `User` with superuser powers.
        Superuser powers means that this use is an admin that can do anything
        they want.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True, default="default-username")
    email = models.EmailField(db_index=True, unique=True)
    photo = models.ImageField(blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField("image", blank=True, null=True, default='https://www.google.com/imgres?imgurl=https%3A%2F%2Fmiro')
    first_name = models.CharField(max_length=30,blank=True, null=True)
    last_name = models.CharField(max_length=50,blank=True, null=True)
    contact = models.PositiveSmallIntegerField(blank=False, null=True)
    gen = (
         ('Male', 'Male'),
         ('Female', 'Female')
        )
    gender  = models.CharField(max_length=65, choices=gen)
    bio = models.TextField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return '{}'.format(self.user.username)

def create_profile_post_receiver(sender, instance, *args, **kwargs):
    if kwargs['created']:
       instance.profile = Profile.objects.create(user=instance)

post_save.connect(create_profile_post_receiver, sender=User)

