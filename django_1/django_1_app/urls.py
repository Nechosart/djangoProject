from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('login/', views.LoginPage.as_view(), name='login'),
    path('postCreate/', views.post_create_page, name='postCreate'),
    path('post/<int:id>/', views.PostView.as_view(), name='post'),
    path('users/', views.UsersView.as_view(), name='users'),
    path('user/<int:id>/', views.UserView.as_view(), name='user'),
    path('chatNew/<int:id>/', login_required(views.ChatNewView.as_view()), name='chatNew'),
    path('chat/<int:id>/', login_required(views.ChatView.as_view()), name='chat')
   # path('chat/', views.ChatView.as_view(), name='chat'),
   # path('history/', views.HistoryView.as_view(), name='history'),
]
