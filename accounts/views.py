from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
# Create your views here.

def signup(request):
    if request.user.is_authenticated:
        return redirect('posts:index')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('posts:index')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }

    return render(request, 'accounts/form.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('posts:index')
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            next_url = request.GET.get('next')
            return redirect(next_url or 'posts:index')
    else:
        form = CustomAuthenticationForm()

    context = {
        'form': form,
    }

    return render(request, 'accounts/form.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('accounts:login')

def profile(request, username, choice):
    User = get_user_model()
    user_info = User.objects.get(username=username)

    if choice==1:
        myselect = True
    else:
        myselect = False
    context = {
        'user_info': user_info,
        'choice': myselect,
    }
    
    return render(request, 'profile.html', context)

@login_required
def follow(request, username):
    me = request.user
    you = get_user_model().objects.get(username=username)
    if you in me.followings.all():
        me.followings.remove(you)
        status = False
    else:
        me.followings.add(you)
        status = True
    context = {
        'status': status,
        'count': len(you.followers.all()),
    }

    return JsonResponse(context)

# def follow_async(request, post_id):
#     user = request.user
#     post = Post.objects.get(id=post_id)
#     if post in user.like_posts.all():
#         post.like_users.remove(user)
#         status = False
#     else:
#         post.like_users.add(user)
#         status = True

#     context = {
#         'status': status,
#         'count': len(post.like_users.all()),
#     }

#     return JsonResponse(context)