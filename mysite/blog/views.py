from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import PostForm, CommentForm, LoginForm, RegisterForm
from .models import Post, Comment


# Create your views here.


def feed(request):
    posts = Post.objects.all().order_by('-publish')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger or EmptyPage:
        posts = paginator.page(1)

    return render(request, 'feed.html', {'posts': posts, 'page': page_number, 'user': request.user})


def post(request, post_id):
    post_by_id = Post.objects.get(id=post_id)
    if not post_by_id:
        return HttpResponse('error')

    if request.method == "GET":
        form = CommentForm()
        comments = Comment.objects.filter(post=post_by_id).order_by('-publish')
        paginator = Paginator(comments, 10)
        page_number = request.GET.get('page')
        try:
            comments = paginator.page(page_number)
        except PageNotAnInteger or EmptyPage:
            comments = paginator.page(1)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            Comment.objects.create(post=post_by_id, text=form_data['text'], user=request.user)
            return HttpResponseRedirect(f"/blog/post/{post_id}")

    return render(request, 'post.html', {'post': post_by_id, 'comments': comments, 'page': page_number, 'form': form})


@login_required(login_url='/blog/login')
def create_post(request):
    if request.method == "GET":
        form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            Post.objects.create(title=form_data['title'], text=form_data['text'],
                                user=request.user)
            return HttpResponseRedirect('/blog')
    return render(request, 'create_post.html', {'form': form})


def login_user(request):
    message = ""
    if request.method == "GET":
        form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            user = authenticate(username=form_data['username'], password=form_data['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect('/blog')
            message = "Неверные данные"
    return render(request, 'login.html', {'form': form, 'message': message})


@login_required(login_url='/blog/login')
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/blog')


def register_user(request):
    message = ""
    if request.method == "GET":
        form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            if not User.objects.filter(username=form_data['username']).count():
                user = User.objects.create(username=form_data['username'], password=make_password(form_data['password']))
                login(request, user)
                return HttpResponseRedirect('/blog')
            else:
                message = "Пользователь с таким именем уже существует"
    return render(request, 'register.html', {'form': form, 'message': message})