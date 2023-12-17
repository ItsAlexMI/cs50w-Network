from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def index(request):
    all_posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(all_posts, 10)  

    page_number = request.GET.get('page')
    
    page_obj = paginator.get_page(page_number)

    
    liked_posts = []
    logged_in_user = request.user if request.user.is_authenticated else None


    if request.user.is_authenticated:
        liked_posts = Like.objects.filter(user=request.user).values_list('post__id', flat=True)

    return render(request, 'network/index.html', {
        'page_obj': page_obj,
        'liked_posts': liked_posts,
        'logged_in_user': logged_in_user
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def new_post (request):
    if request.method == "POST":
        user = request.user
        content = request.POST["content"]
        post = Post(user=user, content=content)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    return httpResponseRedirect(reverse("index"))


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        content = request.POST["content"]
        post.content = content
        post.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "network/edit_post.html", {
        "post": post
    })

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    like, created = Like.objects.get_or_create(user=user, post=post)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    like_count = post.like_set.count()
    
    return JsonResponse({'liked': liked, 'like_count': like_count})

def get_like_count(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like_count = post.like_set.count()
    return JsonResponse({'like_count': like_count})

def comment (request, post_id): 
    
    posts = Post.objects.all()
    post = get_object_or_404(Post, id=post_id)
    liked_posts = []  
    
    comentarios = Comment.objects.filter(post=post)

    logged_in_user = request.user if request.user.is_authenticated else None


    if request.user.is_authenticated:
        liked_posts = Like.objects.filter(user=request.user).values_list('post__id', flat=True)

    if request.method == "POST":
        user = request.user
        post = get_object_or_404(Post, id=post_id)
        content = request.POST["content"]
        comment = Comment(user=user, post=post, content=content)
        comment.save()
        return HttpResponseRedirect(reverse("comment", args=[post_id]))
    return render (request, "network/comment.html", {
        "post": post,
        "liked_posts": liked_posts,
        "comentarios": comentarios,
        "logged_in_user": logged_in_user
    })


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return HttpResponseRedirect(reverse("index"))
    
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return HttpResponseRedirect(reverse("index"))

@login_required
def seguir_perfil(request, username):
    perfil = get_object_or_404(User, username=username)
    SeguirPerfil.objects.get_or_create(seguidor=request.user, siguiendo=perfil)
    return HttpResponseRedirect(reverse('profile', args=[username]))

@login_required
def dejar_seguir_perfil(request, username):
    perfil = get_object_or_404(User, username=username)
    SeguirPerfil.objects.filter(seguidor=request.user, siguiendo=perfil).delete()
    return HttpResponseRedirect(reverse('profile', args=[username]))


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user).order_by('-created_at') 
    
    paginator = Paginator(posts, 10)  
    page_number = request.GET.get('page')

    if page_number is None:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    
    liked_posts = []
    logged_in_user = request.user if request.user.is_authenticated else None
    is_following = SeguirPerfil.objects.filter(seguidor=logged_in_user, siguiendo=user).exists() if logged_in_user else False
    seguidores = SeguirPerfil.objects.filter(siguiendo=user)
    seguidores_count = seguidores.count()
    seguidos = SeguirPerfil.objects.filter(seguidor=user)
    seguidos_count = seguidos.count()

    if request.user.is_authenticated:
        liked_posts = Like.objects.filter(user=request.user).values_list('post__id', flat=True)

    return render(request, "network/miPerfil.html", {
        "user": user,
        "posts": page_obj,  
        'logged_in_user': logged_in_user,
        'is_following': is_following,
        'liked_posts': liked_posts,
        'seguidores_count': seguidores_count,
        'seguidos_count': seguidos_count,   
        'page_obj': page_obj  
    })

def following(request):
    followed_users = SeguirPerfil.objects.filter(seguidor=request.user).values_list('siguiendo', flat=True)
    posts = Post.objects.filter(user__in=followed_users).order_by('-created_at')
    paginator = Paginator(posts, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    liked_posts = []  
    logged_in_user = request.user if request.user.is_authenticated else None

    if request.user.is_authenticated:
        liked_posts = Like.objects.filter(user=request.user).values_list('post__id', flat=True)

    return render(request, "network/following.html", {
        "posts": page_obj,  
        "liked_posts": liked_posts,
        "logged_in_user": logged_in_user,
        "page_obj": page_obj
    })