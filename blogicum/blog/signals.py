from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment, Post


@receiver(post_save, sender=Comment)
def update_comment_count(sender, instance, created, **kwargs):
    if created:
        Post.objects.filter(pk=instance.publication_id).update(
            comment_count=F('comment_count') + 1
        )
