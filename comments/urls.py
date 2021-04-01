from django.urls import path
from .views import *

urlpatterns = [
    path('api/comments/', CommentView.as_view(), name='comments'),
    path('api/comments/post/', CommentPostView.as_view(), name='article_post'),
    #path('api/comments/delete/<int:pk>/', CommentApiView.as_view(), name='article_delete'),
    
]