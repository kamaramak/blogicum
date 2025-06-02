from datetime import datetime

from django.shortcuts import render, get_object_or_404

from .models import Post, Category
from core.constants import POSTS_ON_MAIN_COUNT


def index(request):
    """Возвращает рендер с переданным списком всех постов"""
    template = 'blog/index.html'
    post_list = Post.objects.select_related(
        'category',
        'author',
        'location',
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lt=datetime.now(),
    )[:POSTS_ON_MAIN_COUNT]
    context = {
        'post_list': post_list,
    }
    return render(request, template, context)


def post_detail(request, id):
    """Возвращает рендер с переданным одним постом соответствующим"""
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.select_related(
            'category',
            'author',
            'location',
        ).filter(
            is_published=True,
            category__is_published=True,
            pub_date__lt=datetime.now(),
        ),
        pk=id
    )
    context = {
        'post': post,
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    """Возвращает рендер с переданной категорией"""
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        is_published=True,
        slug=category_slug,
    )
    post_list = Post.objects.select_related(
        'category',
        'author',
        'location',
    ).filter(
        is_published=True,
        pub_date__lt=datetime.now(),
        category=category,
    )
    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, template, context)
