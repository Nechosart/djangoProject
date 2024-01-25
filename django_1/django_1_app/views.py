from .models import Country, User, Post, Comment, Chat, Message, LikePost, LikeComment
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.views.generic.list import ListView
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import CountryForm, RegistrationForm, LoginForm, PostForm, PostEditForm, CommentForm, MessageForm
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    #context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Instagram'
        context['posts'] = Post.objects.all()
        context['user'] = self.request.user
        # context['cookie'] = self.request.COOKIES['name']
        return context

    def post(self, request, **kwargs):
        post = Post.objects.get(id=request.POST['post'])
        if post.likes.filter(user=request.user):
            post.likes.get(user=request.user).delete()
        else:
            like = LikePost.objects.create(user=request.user)
            post.likes.add(like)
        post.save()
        return JsonResponse(True, safe=False)


class RegistrationView(CreateView):
    template_name = 'registration.html'
    form_class = RegistrationForm

    def get_success_url(self):
        response = HttpResponse()
        response.set_cookie('username', self.object.username)
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
        context['users'] = User.objects.all()
        context['user'] = self.request.user
        # context['cookie'] = self.request.COOKIES['name']
        return context


class UserView(TemplateView):
    template_name = 'user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id=kwargs['id'])
        context['title'] = user.username
        context['person'] = user
        context['posts'] = Post.objects.filter(user=user)
        context['user'] = self.request.user
        return context


@login_required
def post_create_page(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            post = Post(name=name, description=description, user=request.user)
            post.save()
            return redirect('/')
        return redirect('/postCreate')
    else:
        form = PostForm()
        return render(request, 'postCreate.html', {'title': 'New post','user': request.user, 'form': form})


class PostView(TemplateView):
    template_name = 'post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        post = Post.objects.get(id=kwargs['id'])
        context['title'] = post.name
        context['post'] = post
        context['comments'] = Comment.objects.filter(post=kwargs['id'])
        context['form'] = CommentForm()
        context['form1'] = PostEditForm()
        return context

    def post(self, request, **kwargs):
        post = Post.objects.get(id=kwargs['id'])
        typeSend = request.POST['typeSend']
        if typeSend == 1:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = Comment(text=form.cleaned_data['text'], user=request.user)
                post.comments.add(comment)
                post.save()
                resp = {'ok': True, 'comment': comment.text}
            else:
                resp = {'ok': False, 'error': 'Error'}

        elif typeSend == 2:
            form = PostEditForm(request.POST)
            if form.is_valid():
                datas = ['name', 'description']
                for d in datas:
                    if form.cleaned_data[d]:
                        post[d] = form.cleaned_data[d]
                post.save()
                resp = {'ok': True}
            else:
                resp = {'ok': False, 'error': 'Error'}

        elif typeSend == 3:
            if LikePost.objects.get(user=request.user):
                LikePost.objects.get(user=request.user).delete()
            else:
                like = LikePost(user=request.user)
                post.likes.add(like)
            post.save()
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

        talker = chat.user2 if chat.user1 == user else chat.user1
        context['title'] = f'Chat with {talker}'
        context['talker'] = talker
        context['user'] = user
        context['chat'] = chat
        context['messages'] = chat.messages.filter(chat=chat.id)
        context['form'] = MessageForm()
        return context

    def post(self, request, **kwargs):
        form = MessageForm(request.POST)
        if form.is_valid():
            chat = Chat.objects.get(id=kwargs['id'])
            message = Message.objects.create(text=form.cleaned_data['text'], chat=chat, user=self.request.user)
            chat.messages.add(message)
            chat.save()
            resp = f'{message.text}'
        else:
            resp = 'ERROR'
        return JsonResponse(resp, safe=False)
            #post = Post.objects.get(id=kwargs['id'])
            #post.name = data['name']
            #post.save()

# def page1(request):
#     if request.method == 'POST':
#         data = request.POST
#         name = data['name']
#         surname = data['surname']
#         age = data['age']
#         dir = Director(name=name, surname=surname, age=age)
#         dir.save()
#     return render(request, 'page1.html')
#
# def page2(request):
#     dirs = Director.objects.all()
#
#     return render(request, 'page2.html', {'data': dirs})
#
# # CRUD - Create Read Update Delete
# def page3(request):
#     if request.method == 'POST':
#         form = FilmForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data['title']
#             genre = form.cleaned_data['genre']
#             year = form.cleaned_data['year']
#             dir = Director.objects.get(id=1)
#             film = Film(title=name, genre=genre, year=year, director=dir)
#             film.save()
#             return render(request, 'page3.html', {'form': form})
#     else:
#         form = FilmForm()
#         return render(request, 'page3.html', {'form': form})
#
#
# def book_create(request):
#     if request.method == 'POST':
#         form = BookForm1(request.POST)
#         if form.is_valid():
#             title = form.cleaned_data['title']
#             year = form.cleaned_data['year']
#             author = form.cleaned_data['author']
#             book = Book(title=title, year=year, author=author)
#             book.save()
#             return redirect('/create_post')
#     else:
#         form = BookForm1()
#         return render(request, 'page3.html', {'form': form})
#
#
# def  form_page(request):
#     form = LoginForm()
#     return render(request, 'page3.html', {'form': form})
