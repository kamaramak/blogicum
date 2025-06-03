from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import PostForm, CommentForm
from .models import Post, Category, Comment
from core.constants import POSTS_ON_MAIN_COUNT

User = get_user_model()


class BlogListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    queryset = Post.objects.select_related(
        'author', 'location', 'category'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lt=timezone.now(),
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
        pub_date__lt=timezone.now(),
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
            pub_date__lt=timezone.now(),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ProfileDetailView(DetailView):
    model = User
    template_name = 'blog/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username_slug'


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
#         pub_date__lt=timezone.now(),
#         category=category,
#     )
#     context = {
#         'category': category,
#         'post_list': post_list
#     }
#     return render(request, template, context)
