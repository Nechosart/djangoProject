from django import forms
from .models import Country, User, Post, PostEdit, Comment, Message
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
#from django.contrib.auth.models import User


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['name']


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {'username': forms.TextInput(attrs={'id': 'username'}),
                   'email': forms.TextInput(attrs={'id': 'email'})}


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['name', 'description']


class PostEditForm(forms.ModelForm):
    class Meta:
        model = PostEdit
        fields = ['name', 'description']
        widgets = {'name': forms.TextInput(attrs={'id': 'name'}),
                   'description': forms.TextInput(attrs={'id': 'description'})}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {'text': forms.TextInput(attrs={'id': 'text'})}


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        widgets = {'text': forms.TextInput(attrs={'id': 'text'})}


