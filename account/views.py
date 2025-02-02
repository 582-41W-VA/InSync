from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, ProfileImage
from django.shortcuts import render, redirect
from posts.models import Post 
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    SetPasswordForm,
)


@login_required
def index(request):
    if request.method == "POST":
        form = SetPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("account:index")
    else:
        form = SetPasswordForm(user=request.user)
    context = {"form": form}
    return render(request, "account/index.html", context)


def signup(request):
    form = UserCreationForm(request.POST)
    context = {"form": form}
    if request.method == "GET" or not form.is_valid():
        return render(request, "account/signup.html", context)
    form.save()
    return redirect("account:login")
    

def login(request):
    form = AuthenticationForm(request, data=request.POST)
    context = {"form": form}
    if request.method == "GET" or not form.is_valid():
        return render(request, "account/login.html", context)
    user = form.get_user()
    django_login(request, user)
    return redirect("account:index")


@login_required
def update_profile(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=profile)
        profile_img = ProfileImage(request.POST, request.FILES, instance=profile)
        if form.is_valid() and profile_img.is_valid():
            form.save()
            profile_img.save()
            return redirect("account:profile_overview")
    else:
        form = ProfileUpdateForm(instance=profile)
        profile_img = ProfileImage(instance=profile)
    context = { 'form': form, 'profile_img': profile_img, 'profile': profile }
    return render(request, 'account/update_profile.html', context)


@login_required
def profile_overview(request):
    user = request.user
    posts = Post.objects.filter(user=user)
    context = { 'user': user, 'posts': posts }
    return render(request, "account/profile_overview.html", context)


def logout(request):
    django_logout(request)
    return redirect("account:login")
