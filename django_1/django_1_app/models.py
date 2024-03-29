from django.db import models
from django.contrib.auth.models import AbstractUser


class Country(models.Model):
    name = models.CharField(max_length=32)


class Notification(models.Model):
    text = models.CharField(max_length=96)
    href = models.CharField(max_length=64)
    number = models.IntegerField(default=1)
    new = models.BooleanField(default=True)


class Subscribe(models.Model):
    followerId = models.IntegerField()


class User(AbstractUser):
    image = models.ImageField(upload_to='static/images', default='/static/images/base.jpg')
    createdAt = models.DateTimeField(auto_now_add=True)
    notifications = models.ManyToManyField(Notification)
    subscribes = models.ManyToManyField(Subscribe)
#     email = models.EmailField('email', max_length=64, unique=True)
#     USERNAME_FIELD = 'email'
#     year = models.IntegerField('year')
#     # image = models.ImageField(upload_to='static/images')
#     createdAt = models.DateTimeField(auto_now_add=True)
#     country = models.ForeignKey(Country, on_delete=models.CASCADE)


class LikeComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.CharField(max_length=1024)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(LikeComment)


class LikePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Post(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    image = models.ImageField(upload_to='static/images', default='')
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(LikePost)
    comments = models.ManyToManyField(Comment)


class PostEdit(models.Model):
    name = models.CharField(max_length=64, null=True)
    description = models.CharField(max_length=1024, null=True)


class Message(models.Model):
    text = models.CharField(max_length=1024)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Chat(models.Model):
    user1 = models.ForeignKey(User, related_name='user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='user2', on_delete=models.CASCADE)
    messages = models.ManyToManyField(Message)





