from django.urls import path
from . import views

app_name = "posts"
urlpatterns = [
    path("", views.home, name="home"), 
    path('<int:post_id>/', views.post_detail, name='post_detail'), 
    path('create_post/', views.create_post, name='create_post'),

    path('search/', views.search_result, name='search_result'),
    

    path('toggle_save/<str:object>/<int:object_id>/', views.toggle_save, name='toggle_save'),
    path('toggle_upvote/<str:object>/<int:object_id>/', views.toggle_upvote, name='toggle_upvote'),
    path('flag/<str:object>/<int:object_id>/', views.flag, name='flag'),
]