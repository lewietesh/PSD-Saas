# notifications/models.py
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
import re


def validate_word_count(value):
    """Validate that text doesn't exceed 500 words"""
    word_count = len(value.strip().split())
    if word_count > 500:
        raise ValidationError(f'Message exceeds 500 words (currently {word_count} words).')
    return value


def validate_sender_name(value):
    """Validate sender name format"""
    if len(value.strip()) < 2:
        raise ValidationError('Name must be at least 2 characters long.')
    # Only allow letters, spaces, hyphens, and apostrophes
    if not re.match(r"^[a-zA-Z\s\-']+$", value):
        raise ValidationError('Name can only contain letters, spaces, hyphens, and apostrophes.')
    return value


class Message(models.Model):
    """
    Contact messages from website visitors, in-system users, or order communications
    """
    
    SUBJECT_CHOICES = [
        ('general', 'General Inquiry'),
        ('service', 'Service Request'),
        ('consultation', 'Book Free Consultation'),
        ('tutoring', 'Tutoring'),
        ('partnership', 'Partnership'),
        ('order', 'Order Communication'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('lead', 'Lead'),
        ('client', 'Client'),
        ('closed', 'Closed'),
    ]
    
    MESSAGE_TYPE_CHOICES = [
        ('contact', 'Contact Message'),
        ('order', 'Order Message'),
    ]
    
    # Primary fields
    id = models.CharField(
        max_length=36,
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Required fields
    sender_name = models.CharField(
        max_length=255,
        validators=[validate_sender_name]
    )
    email = models.EmailField()
    message = models.TextField(validators=[validate_word_count])
    subject = models.CharField(
        max_length=100,
        choices=SUBJECT_CHOICES,
        default='general'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )
    
    # Message type and order relationship
    message_type = models.CharField(
        max_length=20,
        choices=MESSAGE_TYPE_CHOICES,
        default='contact',
        help_text="Type of message: contact inquiry or order communication"
    )
    order = models.ForeignKey(
        'business.Order',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='messages',
        help_text="If this is an order message, link to the order"
    )
    
    # Optional fields
    phone = models.CharField(max_length=20, blank=True)
    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
        help_text="Auto-captured from request"
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        help_text="Mapped from IP address (future feature)"
    )
    device = models.CharField(
        max_length=255,
        blank=True,
        help_text="User-Agent string from request"
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_messages',
        help_text="Admin user assigned to handle this message"
    )
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='messages',
        help_text="Optional link to in-system user who sent message"
    )
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'message'
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['subject']),
            models.Index(fields=['assigned_to']),
            models.Index(fields=['user_id']),
            models.Index(fields=['created_at']),
            models.Index(fields=['order', 'message_type']),
        ]
    
    def __str__(self):
        return f"{self.sender_name} - {self.get_subject_display()}"
    
    @property
    def word_count(self):
        """Get word count of message"""
        return len(self.message.strip().split())


class MessageReply(models.Model):
    """
    Replies to contact messages (admin responses or client follow-ups)
    """
    
    SENDER_TYPE_CHOICES = [
        ('client', 'Client'),
        ('admin', 'Admin'),
    ]
    
    # Primary fields
    id = models.CharField(
        max_length=36,
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Relationships
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='message_replies'
    )
    
    # Content fields
    sender_name = models.CharField(max_length=255)
    sender_type = models.CharField(
        max_length=20,
        choices=SENDER_TYPE_CHOICES,
        default='admin'
    )
    reply_message = models.TextField(
        max_length=1000,
        help_text="Reply text (max 1000 characters)"
    )
    
    # Timestamp
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'message_reply'
        verbose_name = 'Message Reply'
        verbose_name_plural = 'Message Replies'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['message']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Reply by {self.sender_name} to {self.message.sender_name}"
