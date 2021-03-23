from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Article(models.Model):
    title = models.TextField(max_length =60)
    post = models.CharField(max_length=255)
    image = models.ImageField(upload_to = 'articles/', blank=True)
    editor = models.ForeignKey(User,on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.title