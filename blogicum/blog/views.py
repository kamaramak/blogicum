from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import PostForm, CommentForm
from .models import Post, Category, Comment
from core.constants import POSTS_ON_MAIN_COUNT

User = get_user_model()


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.username == self.request.user.username


class BlogListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    queryset = Post.objects.select_related(
        'author', 'location', 'category'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lt=datetime.now(),
    )
    ordering = '-pub_date'
    paginate_by = 10


class BlogDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    queryset = Post.objects.select_related(
        'category',
        'author',
        'location',
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lt=datetime.now(),
    )


class CategoryListView(ListView):
    model = Post
    template_name = 'blog/category.html'
    ordering = '-pub_date'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(
            Category,
            is_published=True,
            slug=self.kwargs['category_slug']
        )
        return super().get_queryset().select_related(
            'author', 'location', 'category'
        ).filter(
            is_published=True,
            category__is_published=True,
            pub_date__lt=datetime.now(),
            category=self.category
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ProfileListlView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    ordering = '-pub_date'
    paginate_by = 10

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        if self.request.user == user:
            return super().get_queryset().select_related(
                'author', 'location', 'category'
            ).filter(author=user)
        else:
            return super().get_queryset().select_related(
                'author', 'location', 'category'
            ).filter(
                author=user,
                is_published=True,
                pub_date__lt=datetime.now()
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs['username']
        context['profile'] = get_object_or_404(User, username=username)
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    fields = ['username', 'first_name', 'last_name', 'email']
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.object.username}
        )


class BlogCreateView(CreateView):
    pass


# def index(request):
#     """Возвращает рендер с переданным списком всех постов"""
#     template = 'blog/index.html'
#     post_list = Post.objects.select_related(
#         'category',
#         'author',
#         'location',
#     ).filter(
#         is_published=True,
#         category__is_published=True,
#         pub_date__lt=datetime.now(),
#     )[:POSTS_ON_MAIN_COUNT]
#     context = {
#         'post_list': post_list,
#     }
#     return render(request, template, context)


# def post_detail(request, id):
#     """Возвращает рендер с переданным одним постом соответствующим"""
#     template = 'blog/detail.html'
#     post = get_object_or_404(
#         Post.objects.select_related(
#             'category',
#             'author',
#             'location',
#         ).filter(
#             is_published=True,
#             category__is_published=True,
#             pub_date__lt=datetime.now(),
#         ),
#         pk=id
#     )
#     context = {
#         'post': post,
#     }
#     return render(request, template, context)


# def category_posts(request, category_slug):
#     """Возвращает рендер с переданной категорией"""
#     template = 'blog/category.html'
#     category = get_object_or_404(
#         Category,
#         is_published=True,
#         slug=category_slug,
#     )
#     post_list = Post.objects.select_related(
#         'category',
#         'author',
#         'location',
#     ).filter(
#         is_published=True,
#         pub_date__lt=datetime.now(),
#         category=category,
#     )
#     context = {
#         'category': category,
#         'post_list': post_list
#     }
#     return render(request, template, context)
