from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Registration

@receiver(post_save, sender=User)
def create_or_update_registration(sender, instance, created, **kwargs):
    if created:
        Registration.objects.create(user=instance, your_name=instance.username)
    else:
        instance.registration.save()
