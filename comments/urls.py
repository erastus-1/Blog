from django.urls import path
from .views import *

urlpatterns = [
    path('api/comments/comment/', CommentView.as_view(), name='comments'),
    path('api/comments/comment/post/', CommentPostView.as_view(), name='article_post'),
    
]