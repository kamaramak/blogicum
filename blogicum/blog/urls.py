from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path(
        '',
        views.PostListView.as_view(),
        name='index',
    ),
    path(
        'posts/create/',
        views.PostCreateView.as_view(),
        name='create_post',
    ),
    path(
        'posts/<int:pk>/',
        views.PostDetailView.as_view(),
        name='post_detail',
    ),
    path(
        'posts/<int:pk>/edit/',
        views.PostUpdateView.as_view(),
        name='edit_post',
    ),
    path(
        'posts/<int:pk>/delete/',
        views.PostDeleteView.as_view(),
        name='delete_post',
    ),
    path(
        'posts/<int:pk>/comment/',
        views.CommentCreateView.as_view(),
        name='add_comment'
    ),
    path(
        'category/<slug:category_slug>/',
        views.CategoryListView.as_view(),
        name='category_posts',
    ),
    path(
        'profile/<str:username>/',
        views.ProfileListlView.as_view(),
        name='profile',
    ),
    path(
        'profile/edit_profile/',
        views.ProfileUpdateView.as_view(),
        name='edit_profile',
    ),
]
