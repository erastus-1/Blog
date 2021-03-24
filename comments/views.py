from rest_framework.response import Response
from rest_framework.permissions import *
from rest_framework import generics
from django.shortcuts import render
from rest_framework import status
from .serializers import *
from .models import *
import datetime as dt

# Create your views here.
class CommentView(generics.CreateAPIView):
    queryset= Comment.objects.all()
    serializer_class= CommentSerializer
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        all_articles = Comment.objects.all()
        serializers = CommentSerializer(all_articles , many=True)
        return Response(serializers.data)

class CommentPostView(generics.CreateAPIView):
    queryset= Comment.objects.all()
    serializer_class= CommentSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):  
        serializers = CommentSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        comment = self.get_comment(pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
   