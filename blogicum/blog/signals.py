from django.db.models import F
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Comment, Post


@receiver(post_save, sender=Comment)
def update_comment_count(sender, instance, created, **kwargs):
    if created:
        Post.objects.filter(pk=instance.post_id).update(
            comment_count=F('comment_count') + 1
        )


@receiver(post_delete, sender=Comment)
def update_comment_count_on_delete(sender, instance, **kwargs):
    Post.objects.filter(pk=instance.post_id).update(
        comment_count=F('comment_count') - 1
    )
