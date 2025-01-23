from django.shortcuts import render, redirect
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    SetPasswordForm,
)
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required


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


def register(request):
    form = UserCreationForm(request.POST)
    context = {"form": form}
    if request.method == "GET" or not form.is_valid():
        return render(request, "account/register.html", context)
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


def logout(request):
    django_logout(request)
    return redirect("account:login")

def home(request):
    return render(request, "account/home.html")
