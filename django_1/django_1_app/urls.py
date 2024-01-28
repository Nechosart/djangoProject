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
    path('chat/<int:id>/', login_required(views.ChatView.as_view()), name='chat'),
    path('direct', login_required(views.DirectView.as_view()), name='direct'),
    path('notifications', views.notification_page, name='notification'),
    path('interesting', views.InterestingView.as_view(), name='interesting'),
    path('search', views.search_page, name='search'),
    path('subscribers/<int:id>', views.SubscribersView.as_view(), name='subscribers')
   # path('chat/', views.ChatView.as_view(), name='chat'),
   # path('history/', views.HistoryView.as_view(), name='history'),
]
