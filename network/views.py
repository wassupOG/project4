from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime
from django.core.paginator import Paginator
import json
from .models import *


def index(request):
    # Get chunks of posts
    paginated_posts = Paginator(Post.objects.all().order_by('-date'), 10)
    rendered_page = paginated_posts.get_page(request.GET.get('page'))

    if request.user.is_authenticated:
        followed_users = request.user.following_set.values_list('following_id', flat=True)
        liked_posts = request.user.liked_set.values_list('post__id', flat=True)

        return render(request, "network/index.html", {'posts': rendered_page, 'liked': liked_posts, 'followed': followed_users})
    else:
        return render(request, "network/index.html", {'posts': rendered_page})
    

def followed(request):
    followed_users = request.user.following_set.values_list('following_id', flat=True)
    paginated_posts = Paginator(Post.objects.filter(user__id__in=followed_users).order_by('-date'), 10)
    rendered_page = paginated_posts.get_page(request.GET.get('page'))
    liked_posts = request.user.liked_set.values_list('post__id', flat=True)
    
    return render(request, 'network/followed.html', {'posts': rendered_page, 'liked': liked_posts, 'followed': followed_users})


def load_profile(request, username):
    load_user = User.objects.get(username=username)
    paginated_posts = Paginator(Post.objects.filter(user=load_user).order_by('-date'), 10)
    rendered_page = paginated_posts.get_page(request.GET.get('page'))

    posts_count = Post.objects.filter(user=load_user).count()
    followers_count = load_user.followers_set.count()
    following_count = load_user.following_set.count()

    context = {'posts': rendered_page, 'user_profile': load_user, 'followers': followers_count, 'following': following_count, 'posts_count': posts_count}

    if request.user.is_authenticated:
        context['followed'] = request.user.following_set.values_list('following_id', flat=True)
        context['liked'] = request.user.liked_set.values_list('post__id', flat=True)
        try:
            Follower.objects.get(follower=request.user, following=load_user)
            context['follow'] = True
        except Follower.DoesNotExist:
            context['follow'] = False
    
    return render(request, "network/profile.html", context)


# APIs
@csrf_exempt
def submit_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data['user_id']  # Assuming you pass the user_id along with the post data
        text = data['text']

        user = User.objects.get(id=user_id)
        post = Post(user=user, text=text, date=datetime.now())
        post.save()

        return JsonResponse({
            'status': 'success',
            'username': post.user.username,
            'text': post.text,
            'date': post.date.strftime('%b. %d, %Y, %I:%M %p'),
            'likes': post.likes,
            'id': post.id
        })

    return JsonResponse({'status': 'error'})


@csrf_exempt
def follow(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'login_required'})
        
        data = json.loads(request.body)
        following_id = data['following_id']
        following = User.objects.get(id=following_id)
        
        try:
            follow_pair = Follower(follower=request.user, following=following)
            follow_pair.save()
            followers_count = Follower.objects.filter(following=following).count()
            following_count = Follower.objects.filter(follower=following).count()

            return JsonResponse({
                'status': 'followed',
                'followers_count': followers_count,
                'following_count': following_count
            })
        
        except IntegrityError:
            follow_pair = Follower.objects.get(follower=request.user, following=following)
            follow_pair.delete()
            followers_count = Follower.objects.filter(following=following).count()
            following_count = Follower.objects.filter(follower=following).count()

            return JsonResponse({
                'status': 'unfollowed',
                'followers_count': followers_count,
                'following_count': following_count
            })

    return JsonResponse({'status': 'error'})


def load_cs50w(request):
    return render(request, "network/cs50w.html")


@csrf_exempt
def update_likes(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'login_required'})
        
        data = json.loads(request.body)
        post_id = data['id']
        user_id = request.user.id

        post = Post.objects.get(id = post_id)
        user = User.objects.get(id=user_id)
        
        try:
            like = Like.objects.get(user=user, post=post)
            like.delete()
            post.likes -= 1
            post.save()
            return JsonResponse({'status': 'unliked'})
        
        except Like.DoesNotExist:
            like = Like(user=user, post=post)
            like.save()
            post.likes += 1
            post.save()
            return JsonResponse({'status': 'liked'})

    return JsonResponse({'status': 'error'})


@csrf_exempt
def edit(request):
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = data['post_id']
        post = Post.objects.get(id=post_id)

        return JsonResponse({'status': 'success', 'text': post.text})
        
    return JsonResponse({'status': 'error'})


@csrf_exempt
def save(request):
    if request.method == "POST":
        data = json.loads(request.body)
        updated_text = data['updated_text']
        post_id = data['post_id']
        post = Post.objects.get(id=post_id)
        post.text = updated_text
        post.save()

        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'})


# Basics
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
