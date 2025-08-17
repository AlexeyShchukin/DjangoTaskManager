from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task

@receiver(post_save, sender=Task)
def notify_task_status_change(sender, instance: Task, created, **kwargs):
    if created:
        return

    if instance.status != instance.last_notified_status:
        print(f"[Email] notification to user {instance.owner.email}: "
              f"Status of task '{instance.title}' changed to '{instance.status}'.")

        instance.last_notified_status = instance.status
        instance.save(update_fields=['last_notified_status'])


from django.core.mail import send_mail
from django.db import transaction
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Task


@receiver(pre_save, sender=Task)
def task_pre_save_track_old_status(sender, instance, **kwargs):
    if not instance.pk:
        instance._old_status = None
        return

    try:
        old = sender.objects.only('id', 'status').get(pk=instance.pk)
        instance._old_status = old.status
    except sender.DoesNotExist:
        instance._old_status = None


@receiver(post_save, sender=Task)
def task_post_save_notify_status_change(sender, instance, created, **kwargs):
    if created:
        return

    old_status = getattr(instance, '_old_status', None)
    new_status = instance.status

    if old_status == new_status:
        return

    def _send_mail():
        subject = f"Task status changed"
        message = f"Hello, {instance.owner.username},\n\n" \
                  f"Status of your task '{instance.title}' changed  from '{old_status}' to '{new_status}'."
        from_mail = "no-reply@example.com"
        to_mail = [instance.owner.email]

        send_mail(
            subject=subject,
            message=message,
            from_email=from_mail,
            recipient_list=to_mail,
            fail_silently=False
        )
        print(f"[Email] Notification sent to owner {instance.owner.email}: "
              f"Status of task '{instance.title}' -> '{new_status}'")

    transaction.on_commit(_send_mail)
