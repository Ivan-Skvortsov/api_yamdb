from django.db.models import Avg
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from reviews.models import Review


@receiver([post_save, post_delete], sender=Review, dispatch_uid='title_rating')
def update_title_rating(instance, **kwargs):
    """Updates Title instance rating, when related Review instance changed."""
    title = instance.title
    avg_rating = title.reviews.all().aggregate(Avg('score'))
    title.rating = int(avg_rating['score__avg'])
    title.save()
