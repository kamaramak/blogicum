from django.contrib import admin

from .models import Category, Location, Post, Comment


class PostInline(admin.TabularInline):
    model = Post
    extra = 0


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )
    list_display = (
        'name',
        'created_at',
        'is_published',
    )
    list_editable = (
        'is_published',
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'is_published',
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )
    list_display = (
        'title',
        'description',
        'slug',
        'created_at',
        'is_published',
    )
    list_editable = (
        'is_published',
    )
    search_fields = (
        'title__icontains',
        'description__icontains',
    )
    list_filter = (
        'title',
        'is_published',
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = (
        CommentInline,
    )
    list_display = (
        'title',
        'text',
        'author',
        'location',
        'category',
        'pub_date',
        'created_at',
        'is_published',
    )
    list_editable = (
        'is_published',
        'author',
        'location',
        'category',
    )
    search_fields = (
        'title__icontains',
        'text__icontains',
    )
    list_filter = (
        'author',
        'category',
        'location',
        'is_published',
    )
