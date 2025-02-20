from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, ProfileImage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from posts.models import Post, Comment
from .models import Profile
import os
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    SetPasswordForm,
)

@login_required
def change_pass(request):
    user = request.user
    if request.method == "POST":
        form = SetPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password changed successfully please login!")
            return redirect("account:login")
    else:
        form = SetPasswordForm(user=request.user)
    context = {"form": form, 'user': user }
    return render(request, "account/change_pass.html", context)


def signup(request):
    form = UserCreationForm(request.POST)
    context = {"form": form}
    if request.method == "GET" or not form.is_valid():
        return render(request, "account/signup.html", context)
    user = form.save()
    profile = Profile.objects.create(user=user)
    if user.is_superuser:
        profile.job_title = 'Admin'  
        profile.save()
    messages.success(request, "Account created, please login!")
    return redirect("account:login")

    
def login(request):
    form = AuthenticationForm(request, data=request.POST)
    context = {"form": form}
    if request.method == "GET" or not form.is_valid():
        return render(request, "account/login.html", context)
    user = form.get_user()
    django_login(request, user)
    messages.success(request, "Welcome, post something cool")
    return redirect("posts:home")


@login_required
def update_profile(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=profile)
        profile_img = ProfileImage(request.POST, request.FILES, instance=profile)
        if form.is_valid() and profile_img.is_valid():
            if request.FILES.get('profile_image'):
                new_image = request.FILES['profile_image']
                if profile.profile_image:
                    old_image_path = profile.profile_image.path
                    if os.path.isfile(old_image_path):
                        os.remove(old_image_path)
                profile.profile_image = new_image
            form.save()
            profile_img.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect("account:update_profile")
    else:
        form = ProfileUpdateForm(instance=profile)
        profile_img = ProfileImage(instance=profile)
    context = {'form': form, 'profile_img': profile_img, 'profile': profile}
    return render(request, 'account/update_profile.html', context)


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user).order_by('-created_at')
    context = {
        'profile_user': user,
        'posts': posts,
    }
    return render(request, 'account/user_profile.html', context)

def user_profile_comments(request, username):
    user = get_object_or_404(User, username=username)
    comments = Comment.objects.filter(user=user).order_by('-created_at')
    context = {
        'profile_user': user,
        'comments': comments,
    }
    return render(request, 'account/user_profile_comments.html', context)

def logout(request):
    django_logout(request)
    return redirect("account:login")