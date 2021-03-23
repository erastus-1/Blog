from rest_framework.response import Response
from rest_framework.permissions import *
from rest_framework import generics
from django.shortcuts import render
from rest_framework import status
from .serializers import *
from .models import *
import datetime as dt

# Create your views here.
class ArticleView(generics.CreateAPIView):
    queryset= Article.objects.all()
    serializer_class= ArticleSerializer
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        all_articles = Article.objects.all()
        serializers = ArticleSerializer(all_articles , many=True)
        return Response(serializers.data)


class ArticlePostView(generics.CreateAPIView):
    queryset= Article.objects.all()
    serializer_class= ArticleSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):  
        serializers = ArticleSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Article(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        article = self.get_article(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
