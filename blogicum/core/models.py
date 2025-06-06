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
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        ),
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class WithRelations(PublishedStrModel):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='%(class)s',
    )

    class Meta:
        abstract = True
