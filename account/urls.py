from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("profile_overview/", views.profile_overview, name="profile_overview"),
    path('update_profile/', views.update_profile, name='update_profile'),
]