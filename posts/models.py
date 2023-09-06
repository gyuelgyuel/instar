from django.db import models
from django.contrib.auth import get_user_model
from django_resized import ResizedImageField
# Create your models here.

class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    image = ResizedImageField(
        size = [500,500],
        crop = ['middle', 'center'],
        upload_to='image/%Y/%m/%d/'
    )
    like_users = models.ManyToManyField(get_user_model(), related_name='like_posts')

class Comment(models.Model):
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
