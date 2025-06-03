from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.BlogListView.as_view(), name='index'),
    path('posts/<int:pk>/',
         views.BlogDetailView.as_view(),
         name='post_detail'),
    path('category/<slug:category_slug>/',
         views.CategoryListView.as_view(),
         name='category_posts'),
    path('profile/<slug:username_slug>/', views.ProfileDetailView.as_view(), name='profile'),
    path('posts/create/', views.BlogCreateView.as_view(), name='create_post')
]
