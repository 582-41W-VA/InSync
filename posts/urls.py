from django.urls import path
from . import views

app_name = "posts"
urlpatterns = [
    path("", views.home, name="home"), 
    path('search/', views.search_result, name='search_result'),
]