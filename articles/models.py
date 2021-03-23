from django.db import models
from django.conf import settings
from django.utils import timezone
from blog.models import *

# Create your models here.
class Article(models.Model):
    title = models.TextField(max_length =60)
    post = models.CharField(max_length=255)
    image = models.ImageField(upload_to = 'articles/', blank=True)
    editor = models.ForeignKey(User,on_delete=models.CASCADE)
    published_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)

    

    def __str__(self):
        return self.title