from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError

from .models import Broker, BrokerInfo, BatchProduct


@receiver(post_save, sender=User)
def create_broker_info(sender, instance, created, **kwargs):
    """Assign BrokerInfo to my proxy User model"""
    if created:
        if isinstance(instance, Broker):
            BrokerInfo.objects.create(user=instance)


@receiver(post_save, sender=BatchProduct)
def update_product_quantity_on_create(sender, instance, created, **kwargs):
    """Update product quantity when a batch is created or updated."""
    if created:
        instance.product.quantity -= instance.quantity
    else:
        original_quantity = instance.__class__.objects.get(pk=instance.pk).quantity

        difference = instance.quantity - original_quantity
        instance.product.quantity -= difference
    if instance.product.quantity < 0:
        raise ValidationError("Product quantity cannot go negative.")

    instance.product.save()


@receiver(post_delete, sender=BatchProduct)
def update_product_quantity_on_delete(sender, instance, **kwargs):
    """Update product quantity when a batch is deleted."""
    instance.product.quantity += instance.quantity
    instance.product.save()
