from rest_framework.response import Response
from rest_framework.permissions import *
from rest_framework import generics
from django.shortcuts import render
from rest_framework import status
from .serializers import *
from .models import *
import datetime as dt

# Create your views here.
# class ArticleView(generics.DestroyAPIView):
#     queryset= Article.objects.all()
#     serializer_class= ArticleSerializer
#     permission_classes = (AllowAny,)

#     def delete(self, request, pk, format=None):
#         article = self.get_article(pk)
#         article.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class ArticlePostView(generics.ListCreateAPIView):
    queryset= Article.objects.all()
    serializer_class= ArticleSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):  
        serializers = ArticleSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        try:
            article = Article.objects.get(id=pk)
        except:
            article=None
        if article:
            serializer = ArticleSerializer(instance=article, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("Post not found")

    def get(self, request, format=None):
        all_articles = Article.objects.all()
        serializers = ArticleSerializer(all_articles , many=True)
        return Response(serializers.data)

class TagAPIView(generics.ListAPIView):
    queryset = Tags.objects.all()
    serializer_class = TagSerializers
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, *args):
        data = self.get_queryset()
        serializer = self.serializer_class(data, many=True)

        if data:
            return Response({
                'message': 'list_of_tags',
                'tags': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'message': 'tags_not_found',
        }, status=status.HTTP_404_NOT_FOUND)