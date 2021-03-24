from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import *
from blog.models import User
from articles.models import Article, Tags

# Create your models here.
class Comment(models.Model):
    post = models.ForeignKey(Article,blank=True, on_delete=models.CASCADE,related_name='comment')
    user = models.ForeignKey(User, blank=True,on_delete=models.CASCADE, related_name='comment_owner')
    comment=  models.CharField(max_length = 250, blank=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.comment)
