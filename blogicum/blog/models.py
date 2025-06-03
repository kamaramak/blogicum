from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from core.models import WithRelations, PublishedStrModel
from core.constants import MAX_LEN_CHARFIELD


User = get_user_model()


class Location(PublishedStrModel):
    name = models.CharField(
        max_length=MAX_LEN_CHARFIELD,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Category(PublishedStrModel):
    title = models.CharField(
        max_length=MAX_LEN_CHARFIELD,
        verbose_name='Заголовок'
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Post(WithRelations):
    title = models.CharField(
        max_length=MAX_LEN_CHARFIELD,
        verbose_name='Заголовок',
    )
    location = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Местоположение',
        related_name='%(class)s',
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='%(class)s',
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title


class Comment(WithRelations):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='%(class)s',
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']

    def __str__(self):
        return self.text