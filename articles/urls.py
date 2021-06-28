from django.urls import path
from .views import *

urlpatterns = [
    path('api/articles/', ArticlePostView.as_view(), name='articles'),
    path('api/articles/post/', ArticlePostView.as_view(), name='article_post'),
    path('api/articles/update/<int:pk>/', ArticlePostView.as_view(), name='update_post'),
    # path('api/articles/delete/<int:pk>/', ArticleView.as_view(), name='delete_post'),
    path('api/articles/tags/', TagAPIView.as_view(), name="tags"),
]