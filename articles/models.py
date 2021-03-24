from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import *
from blog.models import User
from comments.models import Comment

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length =60)
    post = models.OneToOneField('article',max_length=255,on_delete=models.CASCADE,)
    image = models.ImageField(upload_to = 'articles/', blank=True)
    tags = models.ManyToManyField('articles.Tags')
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="author")
    published_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)    

    def __str__(self):
        return self.title

class Tags(models.Model):
    tag = models.CharField(max_length=120)

    def __str__(self):
        return self.tag

