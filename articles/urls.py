from django.urls import path
from .views import *

urlpatterns = [
    path('api/articles/', ArticleView.as_view(), name='articles'),
    path('api/articles/post/', ArticlePostView.as_view(), name='article_post'),
    path('api/articles/update/<int:pk>/', ArticlePostView.as_view(), name='update_post'),
    path('api/articles/comment/', CommentView.as_view(), name='comments'),
    path('api/articles/comment/post/', CommentPostView.as_view(), name='article_post'),
    
]