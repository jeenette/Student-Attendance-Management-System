from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Class, Notification

@receiver(post_save, sender=Class)
def create_class_notification(sender, instance, created, **kwargs):
    if created:
        message = f'Class "{instance.class_name}" was added.'
    else:
        message = f'Class "{instance.class_name}" was updated.'

    # Create a new notification
    Notification.objects.create(message=message)

@receiver(post_delete, sender=Class)
def delete_class_notification(sender, instance, **kwargs):
    message = f'Class "{instance.class_name}" was deleted.'

    # Create a new notification for deletion
    Notification.objects.create(message=message)
