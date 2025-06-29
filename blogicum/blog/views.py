from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import CommentForm, PostForm
from .models import Category, Comment, Post
from core.constants import PAGE_SIZE
from core.mixins import OnlyAuthorMixin

User = get_user_model()


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    queryset = Post.objects.select_related(
        'author', 'location', 'category'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lt=datetime.now(),
    ).annotate(comment_count=Count('comment'))
    ordering = '-pub_date'
    paginate_by = PAGE_SIZE


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_queryset(self):
        pk = self.kwargs['pk']
        post = get_object_or_404(Post, pk=pk)
        current_queryset = super().get_queryset().select_related(
            'category',
            'author',
            'location',
        ).prefetch_related(
            'comment',
        )
        if self.request.user == post.author:
            return current_queryset
        return current_queryset.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lt=datetime.now(),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comment.select_related('author')
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(OnlyAuthorMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'pk': self.object.pk}
        )


class PostDeleteView(OnlyAuthorMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class CategoryListView(ListView):
    model = Post
    template_name = 'blog/category.html'
    ordering = '-pub_date'
    paginate_by = PAGE_SIZE

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
        ).annotate(comment_count=Count('comment'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ProfileListlView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    ordering = '-pub_date'
    paginate_by = PAGE_SIZE

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        current_queryset = super().get_queryset().select_related(
            'author', 'location', 'category'
        )
        if self.request.user == user:
            return current_queryset.filter(author=user).annotate(
                comment_count=Count('comment')
            )
        return current_queryset.filter(
            author=user,
            is_published=True,
            pub_date__lt=datetime.now()
        ).annotate(comment_count=Count('comment'))

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


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        self.current_post = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'pk': self.current_post.pk}
        )

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.current_post
        return super().form_valid(form)


class CommentUpdateView(OnlyAuthorMixin, UpdateView):
    model = Comment
    template_name = 'blog/comment.html'
    fields = ['text']
    context_object_name = 'comment'
    pk_url_kwarg = 'comment_id'

    def get_object(self):
        comment_id = self.kwargs['comment_id']
        return get_object_or_404(Comment, pk=comment_id)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'pk': self.object.post.pk}
        )


class CommentDeleteView(OnlyAuthorMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'

    def get_object(self):
        comment_id = self.kwargs['comment_id']
        return get_object_or_404(Comment, pk=comment_id)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'pk': self.object.post.pk}
        )
