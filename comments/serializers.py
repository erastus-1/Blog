from .models import *
from rest_framework import serializers

#Add your serializers here.
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
       model = Comment
       fields = "__all__" 
       read_only_fields = ('posted_date', 'modified_date')

    