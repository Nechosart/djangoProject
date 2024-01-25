from django.db import models
from django.contrib.auth.models import User

# test 1

class Country(models.Model):
    name = models.CharField(max_length=32)


class Notification(models.Model):
    text = models.CharField(max_length=96)
    href = models.CharField(max_length=64)


# class User(AbstractUser):
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
    # image = models.ImageField(upload_to='static/images')
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


class Subscribe(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)





