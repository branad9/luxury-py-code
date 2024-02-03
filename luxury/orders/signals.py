from django.template.loader import render_to_string
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver

from home.tasks import email_notification

from .models import Order


@receiver(pre_save, sender=Order)
def order_status_email_notification(sender, instance, **kwargs):
    if instance.pk is not None:
        old_status = sender.objects.get(pk=instance.pk).status
        if instance.status != old_status:
            user = instance.user
            status = instance.status.lower()
            context = {"user": user, "order": instance}
            message = render_to_string("emails/order_status.html", context)
            email_notification(f"Order {status}", message, [user.email])
