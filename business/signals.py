# business/signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Order, OrderActivity, Payment
from notifications.models import Message


@receiver(post_save, sender=Order)
def create_order_message_thread(sender, instance, created, **kwargs):
    """
    Automatically create a message thread when a new order is created.
    This enables communication between client and admin for the order.
    """
    if created:
        Message.objects.create(
            message_type='order',
            order=instance,
            sender_name=instance.client.full_name or instance.client.email,
            email=instance.client.email,
            subject='order',
            message=f'Order #{instance.id} has been created. You can use this thread to communicate about your order.',
            user_id=instance.client,
            status='open'
        )
        
        # Create initial timeline activity
        OrderActivity.objects.create(
            order=instance,
            activity_type='created',
            description=f'Order created by {instance.client.full_name or instance.client.email}',
            created_by=instance.client
        )


@receiver(pre_save, sender=Order)
def track_order_status_changes(sender, instance, **kwargs):
    """Track order status changes in timeline"""
    if instance.pk:
        try:
            old_order = Order.objects.get(pk=instance.pk)
            if old_order.status != instance.status:
                OrderActivity.objects.create(
                    order=instance,
                    activity_type='status_change',
                    description=f'Order status changed from {old_order.status} to {instance.status}',
                    created_by=None  # System change
                )
        except Order.DoesNotExist:
            pass


@receiver(post_save, sender=Payment)
def track_payment_activity(sender, instance, created, **kwargs):
    """Track payment events in order timeline"""
    if created and instance.order:
        OrderActivity.objects.create(
            order=instance.order,
            activity_type='payment',
            description=f'Payment of {instance.currency} {instance.amount} via {instance.method}',
            created_by=instance.user
        )
