from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Post(models.Model):
    photo = CloudinaryField('photo')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    date = models.DateTimeField()
    likes = models.IntegerField(default=0)
    unlikes = models.IntegerField(default=0)


class Like(models.Model):
    who_liked = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None)
    date = models.DateTimeField(default=None)


class Dislike(models.Model):
    who_disliked = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None)
    date = models.DateTimeField(default=None)
