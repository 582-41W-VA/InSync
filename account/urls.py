from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('profile/<str:username>/comments', views.user_profile_comments, name='user_profile_comments'),
    path("change_pass/", views.change_pass, name="change_pass"),
    path('update_profile/', views.update_profile, name='update_profile'),
]