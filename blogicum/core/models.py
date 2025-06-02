from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class PublishedStrModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True


class PostWithRelations(PublishedStrModel):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='%(class)s',
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
        abstract = True
