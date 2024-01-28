from .models import Country, Subscribe, User, Post, Comment, Chat, Message, LikePost, LikeComment, Notification
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.views.generic.list import ListView
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import (CountryForm, RegistrationForm, LoginForm, UserChangeForm, PostForm, PostEditForm, CommentForm,
                    MessageForm, SearchForm)
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from pathlib import Path
from django.core.files import File


def new_image(files):
    with open('django_1_app/static/images/number.txt', 'r') as file:
        number = str(int(file.read()) + 1)
    with open('django_1_app/static/images/number.txt', 'w') as file:
        file.write(number)
    with open(f'django_1_app/static/images/{number}.png', 'wb') as file:
        file.write(files['file'].read())
    return f'/static/images/{number}.png'


def new_notification(user, text, href):
    notification = user.notifications.all()
    if notification and notification.last().text == text:
        print('change')
        notification = notification.last()
        notification.number += 1
        notification.save()
    else:
        print('add')
        user.notifications.add(Notification.objects.create(text=text, href=href, user=user))
        user.save()


def like_post(user, post):
    if post.likes.filter(user=user):
        post.likes.get(user=user).delete()
    else:
        like = LikePost.objects.create(user=user)
        post.likes.add(like)
        if user.id != post.user.id:
            new_notification(user, f'{user.username} has liked your post', f'/post/{post.id}')
    post.save()


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    #context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Instagram'
        user = self.request.user
        context['user'] = user
        posts = Post.objects.all()
        if user.is_authenticated:
            for p in posts:
                p.liked = bool(p.likes.filter(user=user))
            context['notificationsNum'] = len(user.notifications.filter(new=True))
        else:
            context['notificationsNum'] = 0
        context['posts'] = posts

        # context['cookie'] = self.request.COOKIES['name']
        return context

    def post(self, request, **kwargs):
        like_post(request.user, Post.objects.get(id=request.POST['post']))
        return JsonResponse(True, safe=False)


class RegistrationView(CreateView):
    template_name = 'registration.html'
    form_class = RegistrationForm

    def get_success_url(self):
        response = HttpResponse()
        response.set_cookie('username', self.object.username)

        if self.request.FILES.get('file'):
            print('exists')
            image = new_image(self.request.FILES)
            user = self.object
            user.image = image
            user.save()

        login(self.request, self.object)
        return '/'


# class LoginPage(LoginView):
    # template_name = 'login.html'
    # form_class = LoginForm
    # redirect_authenticated_user = True


class LoginPage(TemplateView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        context['form'] = LoginForm()
        context['user'] = self.request.user
        return context

    def post(self, request, **kwargs):
        form = LoginForm(self.request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is None:
                resp = {'ok': False, 'text': 'This user or this password is invalid'}
            else:
                login(request, user)
                resp = {'ok': True}
        else:
            resp = {'ok': False, 'text': 'Please fill all fields correctly'}
        return JsonResponse(resp, safe=False)


class LogoutPage(LogoutView):
    pass


class UsersView(ListView):
    model = Post
    template_name = 'users.html'
    #context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'People'
        user = self.request.user
        context['user'] = user
        if user.is_authenticated:
            context['notificationsNum'] = len(user.notifications.filter(new=True))
        else:
            context['notificationsNum'] = 0
        context['users'] = User.objects.annotate(s_count=Count('subscribes')).order_by('-s_count')[:7]
        # context['cookie'] = self.request.COOKIES['name']
        return context


class UserView(TemplateView):
    template_name = 'user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id=kwargs['id'])
        context['title'] = user.username
        context['person'] = user
        context['subscribers'] = user.subscribes.all()
        context['subscribed'] = user.subscribes.filter(followerId=self.request.user.id).exists()
        posts = reversed(list(Post.objects.filter(user=user)))

        user = self.request.user
        context['user'] = user
        if user.is_authenticated:
            context['notificationsNum'] = len(user.notifications.filter(new=True))
        else:
            context['notificationsNum'] = 0

        for p in posts:
            p.liked = bool(p.likes.filter(user=user))
        context['posts'] = posts
        context['form'] = UserChangeForm
        return context

    def post(self, request, **kwargs):
        typeSend = request.POST['typeSend']
        if typeSend == 'like':
            like_post(request.user, request.POST['post'])

        elif typeSend == 'subscribe':
            user = User.objects.get(id=kwargs['id'])
            if user.subscribes.filter(followerId=request.user.id):
                user.subscribes.get(followerId=request.user.id).delete()
            else:
                subscribe = Subscribe.objects.create(followerId=request.user.id)
                user.subscribes.add(subscribe)

                text = f'{self.request.user.username} has subscribed to your channel'
                href = f'/user/{self.request.user.id}'
                new_notification(user, text, href)
            user.save()

        elif typeSend == 'userEdit':
            user = User.objects.get(id=kwargs['id'])
            data = request.POST

            if data.get('username') and not data['username']:
                print('username')
                user.username = data['username']
            if data.get('email') and not data['email']:
                print('email')
                user.email = data['email']
            if self.request.FILES.get('file'):
                user.image = new_image(self.request.FILES)

            user.save()

        return JsonResponse(True, safe=False)


@login_required
def post_create_page(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            user = request.user

            post = Post(name=name, description=description, user=user)
            if request.FILES.get('file'):
                post.image = new_image(request.FILES)
            post.save()

            for s in user.subscribes.all():
                new_notification(User.objects.get(id=s.followerId),
                                 f'{user.username} published new post!', f'/post/{post.id}')

            return redirect('/')
        return redirect('/postCreate')
    else:
        form = PostForm()
        user = request.user
        notificationsNum = len(user.notifications.filter(new=True))
        return render(request, 'postCreate.html', {'title': 'New post', 'user': user,
                                                   'notificationsNum': notificationsNum, 'form': form})


class PostView(TemplateView):
    template_name = 'post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        if user.is_authenticated:
            context['notificationsNum'] = len(user.notifications.filter(new=True))
        else:
            context['notificationsNum'] = 0
        post = Post.objects.get(id=kwargs['id'])
        context['title'] = post.name
        context['p'] = post
        context['comments'] = reversed(list(post.comments.all()))
        context['form'] = CommentForm()
        context['form1'] = PostEditForm()
        return context

    def post(self, request, **kwargs):
        post = Post.objects.get(id=kwargs['id'])
        typeSend = request.POST['typeSend']

        if typeSend == 'comment':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = Comment.objects.create(text=form.cleaned_data['text'], user=request.user)
                post.comments.add(comment)
                post.save()

                if post.user.id != request.user.id:
                    text = f'Message from {self.request.user.username}'
                    href = f'/post/{post.id}'
                    new_notification(post.user, text, href)

                resp = {'ok': True, 'text': comment.text, 'createdAt': comment.createdAt.strftime("%b, %d, %Y, %I%p"),
                        'user': {'id': comment.user.id, 'username': comment.user.username}}
            else:
                resp = {'ok': False, 'error': 'Error'}

        elif typeSend == 'postEdit':
            data = request.POST

            if data.get('name'):
                post.name = data['name']
            if data.get('description'):
                post.description = data['description']
            if self.request.FILES.get('file'):
                post.image = new_image(self.request.FILES)

            post.save()
            resp = {'ok': True}

        elif typeSend == 'like':
            like_post(request.user, post)
            resp = True

        return JsonResponse(resp, safe=False)


class ChatNewView(TemplateView):
    template_name = 'chat.html'

    #@login_required
    def get(self, request, **kwargs):
        if self.kwargs['id'] == self.request.user.id:
            return redirect('/')
        else:
            chat = Chat.objects.filter(user1=User.objects.get(id=self.kwargs['id']), user2=self.request.user)
            if not chat:
                chat = Chat.objects.filter(user2=User.objects.get(id=self.kwargs['id']), user1=self.request.user)
                if not chat:
                    chat = Chat(user1=self.request.user, user2=User.objects.get(id=self.kwargs['id']))
                    chat.save()
                else:
                    chat = chat[0]
            else:
                chat = chat[0]
            return redirect(f'/chat/{chat.id}')


class ChatView(TemplateView):
    template_name = 'chat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chat = Chat.objects.get(id=self.kwargs['id'])
        user = self.request.user
        if not chat or (chat.user1 != user and chat.user2 != user):
            return redirect('/')
        context['user'] = user
        if user.is_authenticated:
            context['notificationsNum'] = len(user.notifications.filter(new=True))
        else:
            context['notificationsNum'] = 0

        talker = chat.user2 if chat.user1 == user else chat.user1
        context['title'] = f'Chat with {talker}'
        context['talker'] = talker
        context['user'] = user
        context['chat'] = chat
        context['messages'] = chat.messages.filter(chat=chat.id)
        context['form'] = MessageForm()
        return context

    def post(self, request, **kwargs):
        Notification.objects.all().delete()

        form = MessageForm(request.POST)
        if form.is_valid():
            chat = Chat.objects.get(id=kwargs['id'])
            message = Message.objects.create(text=form.cleaned_data['text'], chat=chat, user=self.request.user)
            chat.messages.add(message)
            chat.save()

            user = chat.user2 if chat.user1 == self.request.user else chat.user1
            text = f'Message from {self.request.user.username}'
            href = f'/chat/{chat.id}'
            new_notification(user, text, href)

            resp = {'text': message.text, 'createdAt': message.createdAt.strftime("%b, %d, %Y, %I%p"),
                    'user': {'id': message.user.id, 'username': message.user.username}}
        else:
            resp = 'ERROR'
        return JsonResponse(resp, safe=False)
            #post = Post.objects.get(id=kwargs['id'])
            #post.name = data['name']
            #post.save()


class DirectView(TemplateView):
    template_name = 'direct.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['title'] = 'Direct'
        context['user'] = user
        if user.is_authenticated:
            context['notificationsNum'] = len(user.notifications.filter(new=True))
        else:
            context['notificationsNum'] = 0
        context['chats'] = Chat.objects.filter(user1=user.id) | Chat.objects.filter(user2=user.id)
        return context

    def post(self, request, **kwargs):
        pass


@login_required
def notification_page(request):
    notifications = reversed(list(request.user.notifications.all()).copy())
    for n in request.user.notifications.all():
        if n.new:
            n.new = False
            n.save()
    return render(request, 'notifications.html',
                  {'title': 'Notifications', 'user': request.user,
                   'notifications': notifications})


class InterestingView(TemplateView):
    template_name = 'interesting.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        if user.is_authenticated:
            context['notificationsNum'] = len(user.notifications.filter(new=True))
        else:
            context['notificationsNum'] = 0

        context['title'] = 'interesting'

        posts = Post.objects.annotate(l_count=Count('likes')).order_by('-l_count')[:7]
        for p in posts:
            p.liked = bool(p.likes.filter(user=self.request.user))
        context['posts'] = posts
        return context

    def post(self, request, **kwargs):
        typeSend = request.POST['typeSend']
        if typeSend == 'like':
            post = Post.objects.get(id=request.POST['post'])
            if post.likes.filter(user=request.user):
                post.likes.get(user=request.user).delete()
            else:
                like = LikePost.objects.create(user=request.user)
                post.likes.add(like)
            post.save()
        return JsonResponse(True, safe=False)


@login_required
def search_page(request):
    if request.method == 'POST':
        posts = Post.objects.filter(name__contains=request.POST['search'])
    else:
        posts = Post.objects.annotate(l_count=Count('likes')).order_by('-l_count')[:7]

    for p in posts:
        p.liked = bool(p.likes.filter(user=request.user))

    user = request.user
    if user.is_authenticated:
        notificationsNum = len(user.notifications.filter(new=True))
    else:
        notificationsNum = 0

    return render(request, 'search.html',
                  {'title': 'Notifications', 'user': request.user, 'posts': posts,
                   'notifications': notificationsNum, 'form': SearchForm()})


class SubscribersView(ListView):
    template_name = 'users.html'
    #context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{User.objects.get(id=kwargs['id']).username} subscribers'

        user = self.request.user
        context['user'] = user
        if user.is_authenticated:
            context['notificationsNum'] = len(user.notifications.filter(new=True))
        else:
            context['notificationsNum'] = 0

        users = [User.objects.get(id=s.followerId) for s in User.objects.get(id=kwargs['id']).subscribes.all()]
        context['users'] = users
        return context



