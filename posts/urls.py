from django.urls import path
from . import views

app_name = "posts"
urlpatterns = [
    path("", views.home, name="home"), 
    path('<int:post_id>/', views.post_detail, name='post_detail'), 
    path('search/', views.search_result, name='search_result'),
    path('tag/<int:tag_id>/', views.category, name='category'),

    path('create_post/', views.create_post, name='create_post'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    
    path('<int:post_id>/create_comment/', views.create_comment, name='create_comment'),
    path('<int:post_id>/edit_comment/', views.edit_comment, name='edit_comment'),
    path('<int:post_id>/delete_comment/', views.delete_comment, name='delete_comment'),

    path('toggle_save/<str:object>/<int:object_id>/', views.toggle_save, name='toggle_save'),
    path('toggle_upvote/<str:object>/<int:object_id>/', views.toggle_upvote, name='toggle_upvote'),
    path('flag/<str:object>/<int:object_id>/', views.flag, name='flag'),

    path('all_posts/<int:user_id>/', views.all_posts, name='all_posts'),
    path('liked_posts/', views.liked_posts, name='liked_posts'),
    path('saved_posts/', views.saved_posts, name='saved_posts'),
    path('saved_comments/', views.saved_comments, name='saved_comments'),
    path('liked_comments/', views.liked_comments, name='liked_comments'),
]