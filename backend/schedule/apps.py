from django.apps import AppConfig
from django.db.models.signals import post_delete
from django.dispatch import receiver

@receiver(post_delete)
def delete_empty_categories(sender, instance, using, **kwargs):
    from schedule.models import Event
    if type(instance) == Event:
        category = instance.category
        if len(category.event_set.all()) == 0:
            category.delete()

class ScheduleConfig(AppConfig):
    name = 'schedule'
