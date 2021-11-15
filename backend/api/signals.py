from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver

from api.models import Match, News
from  api import make_auxilary_index

@receiver(post_save, sender=Match)
def my_handler(sender, instance, **kwargs):
    if not instance.finished:
        return
    if instance.guest_score < instance.host_score:
        instance.host.score += 3
    elif instance.guest_score == instance.host_score:
        instance.guest.score += 1
        instance.host_score += 1
    else:
        instance.guest.score += 3
    instance.host.save()
    instance.guest.save()
new_docs = []
@receiver(post_save, sender=News)
def search_engine_handler(sender, instance, **kwargs):
    new_docs.append(instance.id)
    make_auxilary_index.make_auxilary_index(new_docs)