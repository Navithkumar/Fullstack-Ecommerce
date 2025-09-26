from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Products
from .services import clear_cache

@receiver(post_save, sender=Products)
def clear_cache_on_save(sender, instance, **kwargs):
    clear_cache()

@receiver(post_delete, sender=Products)
def clear_cache_on_delete(sender, instance, **kwargs):
    clear_cache()
