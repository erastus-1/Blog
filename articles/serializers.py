from .models import *
from rest_framework import serializers
from django.contrib.auth import authenticate

#Add your serializers here.
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
       model = Article
       fields = "__all__" 
       read_only_fields = ('published_date', 'modified_date')

class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('tag',)

    def to_representation(self, instance):
        return instance.tag