# samsapp/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ClassList, Notification

@receiver(post_save, sender=ClassList)
def create_classlist_notification(sender, instance, created, **kwargs):
    if created:
        message = f'Class "{instance.name}" was added.'
    else:
        message = f'Class "{instance.name}" was updated.'

    # Create a new notification
    Notification.objects.create(message=message)

@receiver(post_delete, sender=ClassList)
def delete_classlist_notification(sender, instance, **kwargs):
    message = f'Class "{instance.name}" was deleted.'

    # Create a new notification for deletion
    Notification.objects.create(message=message)
