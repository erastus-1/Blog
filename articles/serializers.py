from .models import *
from rest_framework import serializers
from .models import Shopping
from django.contrib.auth import authenticate

#Add your serilivers here.
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
       model = Article
       fields = "__all__" 
       read_only_fields = ('published_date')