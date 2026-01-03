# notifications/models.py
import uuid
import os
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
import re


# Validators
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


def validate_attachment_size(value):
    """Validate attachment file size (max 5MB per file)"""
    filesize = value.size
    if filesize > 5 * 1024 * 1024:  # 5MB
        raise ValidationError("The maximum file size that can be uploaded is 5MB per file.")
    return value


def validate_thread_total_size(message_instance):
    """Validate total size of all attachments in a message thread (max 100MB)"""
    total_size = sum(attachment.file_size for attachment in message_instance.attachments.all())
    if total_size > 100 * 1024 * 1024:  # 100MB
        raise ValidationError("Total attachment size for this message thread cannot exceed 100MB.")


def message_attachment_path(instance, filename):
    """Generate file path for message attachments"""
    return f'messages/{instance.message.id}/{filename}'


def general_message_attachment_path(instance, filename):
    """Generate file path for general message attachments"""
    return f'general_messages/{instance.general_message.id}/{filename}'


# ==================== CONTACT MESSAGE MODEL (moved from business app) ====================
class ContactMessage(models.Model):
    """
    Contact form submissions for lead capture from external visitors
    Simple contact form messages that don't require threading
    """
    
    SOURCE_CHOICES = [
        ('website', 'Website'),
        ('whatsapp', 'WhatsApp'),
        ('referral', 'Referral'),
        ('social_media', 'Social Media'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    # Primary fields
    id = models.CharField(
        max_length=36, 
        primary_key=True, 
        default=uuid.uuid4,
        editable=False
    )
    
    # Contact information
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    
    # Message content
    subject = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    
    # Tracking fields
    source = models.CharField(
        max_length=50,
        choices=SOURCE_CHOICES,
        default='website'
    )
    is_read = models.BooleanField(default=False)
    replied = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    
    # Optional admin response (single reply only)
    admin_reply = models.TextField(
        blank=True,
        help_text="Admin's response to this contact message"
    )
    replied_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contact_message_replies',
        help_text="Admin user who replied to this message"
    )
    replied_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the admin replied"
    )
    
    # Timestamp
    date_created = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'contact_message'
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
        ordering = ['-date_created']
        indexes = [
            models.Index(fields=['is_read']),
            models.Index(fields=['replied']),
            models.Index(fields=['priority']),
            models.Index(fields=['source']),
        ]
    
    def __str__(self):
        return f"Contact from {self.name} - {self.subject}"


# ==================== GENERAL MESSAGE MODEL (for external messages with subjects) ====================
class GeneralMessage(models.Model):
    """
    General inquiry messages from external visitors with subject categorization
    These are more formal inquiries that allow ONE admin reply and ONE file attachment
    """
    
    SUBJECT_CHOICES = [
        ('general', 'General Inquiry'),
        ('service', 'Service Request'),
        ('consultation', 'Book Free Consultation'),
        ('tutoring', 'Tutoring'),
        ('partnership', 'Partnership'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('lead', 'Lead'),
        ('client', 'Client'),
        ('closed', 'Closed'),
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
    phone = models.CharField(max_length=20, blank=True)
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
    
    # Tracking fields
    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
        help_text="Auto-captured from request"
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        help_text="Mapped from IP address"
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
        related_name='assigned_general_messages',
        help_text="Admin user assigned to handle this message"
    )
    
    # Single admin reply (limit: one reply only)
    admin_reply = models.TextField(
        blank=True,
        help_text="Admin's response to this inquiry (one reply only)"
    )
    replied_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='general_message_replies',
        help_text="Admin user who replied"
    )
    replied_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the admin replied"
    )
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'general_message'
        verbose_name = 'General Message'
        verbose_name_plural = 'General Messages'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['subject']),
            models.Index(fields=['assigned_to']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.sender_name} - {self.get_subject_display()}"
    
    @property
    def word_count(self):
        """Get word count of message"""
        return len(self.message.strip().split())


class GeneralMessageAttachment(models.Model):
    """
    Single file attachment for general messages (limit: ONE per message)
    Allowed: images, PDF, TXT, Word documents; Max: 5MB
    """
    id = models.CharField(
        max_length=36,
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    general_message = models.OneToOneField(
        GeneralMessage,
        on_delete=models.CASCADE,
        related_name='attachment',
        help_text="One attachment per general message"
    )
    
    file = models.FileField(
        upload_to=general_message_attachment_path,
        validators=[
            validate_attachment_size,
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'pdf', 'txt', 'doc', 'docx']
            )
        ],
        help_text="Allowed: images, PDF, TXT, Word (max 5MB)"
    )
    
    original_filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField(help_text="File size in bytes")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'general_message_attachment'
        verbose_name = 'General Message Attachment'
        verbose_name_plural = 'General Message Attachments'
    
    def __str__(self):
        return f"{self.original_filename} ({self.file_size} bytes)"
    
    def save(self, *args, **kwargs):
        if not self.original_filename and self.file:
            self.original_filename = os.path.basename(self.file.name)
        if not self.file_size and self.file:
            self.file_size = self.file.size
        super().save(*args, **kwargs)


# ==================== CONVERSATION MODEL (for tracking chat threads) ====================
class Conversation(models.Model):
    """
    Explicit conversation thread tracking.
    - Order conversations: Auto-created when an Order is created (requires user)
    - General conversations: Created when user starts their first general chat
    - Anonymous conversations: For unauthenticated visitors (identified by session_id)
    Each authenticated user has exactly ONE general conversation and ONE conversation per order.
    Anonymous users are tracked via session_id stored in their browser.
    """
    
    CONVERSATION_TYPE_CHOICES = [
        ('order', 'Order Conversation'),
        ('general', 'General Support'),
        ('anonymous', 'Anonymous Support'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('archived', 'Archived'),
    ]
    
    # Primary fields
    id = models.CharField(
        max_length=36,
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Conversation metadata
    conversation_type = models.CharField(
        max_length=20,
        choices=CONVERSATION_TYPE_CHOICES,
        default='general',
        help_text="Type of conversation: order, general, or anonymous support"
    )
    
    title = models.CharField(
        max_length=255,
        blank=True,
        help_text="Display title for the conversation"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )
    
    # Relationships - user is now optional for anonymous conversations
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conversations',
        null=True,
        blank=True,
        help_text="User who owns this conversation (null for anonymous)"
    )
    
    order = models.OneToOneField(
        'business.Order',
        on_delete=models.CASCADE,
        related_name='conversation',
        null=True,
        blank=True,
        help_text="Associated order (for order conversations). OneToOne ensures one conversation per order."
    )
    
    # Anonymous user tracking fields
    session_id = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        db_index=True,
        help_text="Session ID for anonymous users (stored in their browser localStorage)"
    )
    
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text="IP address of anonymous user (for rate limiting and abuse prevention)"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_message_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp of the last message in this conversation"
    )
    
    class Meta:
        db_table = 'conversation'
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversations'
        ordering = ['-last_message_at', '-created_at']
        indexes = [
            models.Index(fields=['user', 'conversation_type']),
            models.Index(fields=['order']),
            models.Index(fields=['status']),
            models.Index(fields=['last_message_at']),
            models.Index(fields=['session_id']),
        ]
        # Note: Unique constraints with conditions are not supported by MySQL.
        # Uniqueness is enforced at application level via get_or_create_general()
        # and get_or_create_anonymous() methods which use atomic get_or_create.
    
    def __str__(self):
        if self.conversation_type == 'order' and self.order:
            order_num = self.order.order_number or str(self.order.id)[:8]
            return f"Order #{order_num} - {self.user.email if self.user else 'Unknown'}"
        if self.conversation_type == 'anonymous':
            return f"Anonymous - {self.session_id[:8] if self.session_id else 'Unknown'}..."
        return f"General Support - {self.user.email if self.user else 'Unknown'}"
    
    @property
    def is_anonymous(self):
        """Check if this is an anonymous conversation"""
        return self.conversation_type == 'anonymous' and self.user is None
    
    @property
    def unread_count(self):
        """Count of unread messages in this conversation"""
        return self.messages.filter(is_read=False).exclude(sender='user').count()
    
    @classmethod
    def get_or_create_general(cls, user):
        """
        Get or create the user's general support conversation.
        Each user has exactly ONE general conversation.
        """
        conversation, created = cls.objects.get_or_create(
            user=user,
            conversation_type='general',
            defaults={
                'title': 'General Support',
                'status': 'active'
            }
        )
        return conversation, created
    
    @classmethod
    def get_or_create_anonymous(cls, session_id, ip_address=None):
        """
        Get or create an anonymous support conversation.
        Each session_id has exactly ONE anonymous conversation.
        Anonymous conversations expire after 48 hours (handled client-side).
        """
        conversation, created = cls.objects.get_or_create(
            session_id=session_id,
            conversation_type='anonymous',
            defaults={
                'title': 'Anonymous Support',
                'status': 'active',
                'ip_address': ip_address
            }
        )
        # Update IP if it changed
        if not created and ip_address and conversation.ip_address != ip_address:
            conversation.ip_address = ip_address
            conversation.save(update_fields=['ip_address', 'updated_at'])
        return conversation, created
    
    @classmethod
    def create_for_order(cls, order):
        """
        Create a conversation for an order.
        Called automatically via signal when Order is created.
        """
        conversation = cls.objects.create(
            user=order.client,
            order=order,
            conversation_type='order',
            title=f'Order #{order.order_number or str(order.id)[:8]}',
            status='active'
        )
        return conversation


# ==================== MESSAGE MODEL (for in-system users and anonymous) ====================
class Message(models.Model):
    """
    Messages for both authenticated users and anonymous visitors
    Supports 'general', 'order', and 'anonymous' message types
    Both user messages and support replies are stored as Message records
    Anonymous messages have restrictions: no file attachments
    """
    
    MESSAGE_TYPE_CHOICES = [
        ('order', 'Order Message'),
        ('general', 'General Support'),
        ('anonymous', 'Anonymous Support'),
    ]
    
    SENDER_CHOICES = [
        ('user', 'User'),
        ('support', 'Support'),
        ('system', 'System'),
        ('anonymous', 'Anonymous User'),
    ]
    
    # Primary fields
    id = models.CharField(
        max_length=36,
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Conversation reference - groups messages into threads
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        null=True,
        blank=True,
        help_text="The conversation this message belongs to"
    )
    
    # Message metadata
    message_type = models.CharField(
        max_length=20,
        choices=MESSAGE_TYPE_CHOICES,
        default='general',
        help_text="Type of message: order, general, or anonymous support"
    )
    
    sender = models.CharField(
        max_length=20,
        choices=SENDER_CHOICES,
        default='user',
        help_text="Who sent the message"
    )
    
    # Relationships - user is optional for anonymous messages
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_messages',
        null=True,
        blank=True,
        help_text="Authenticated user who owns this message (null for anonymous)"
    )
    
    order = models.ForeignKey(
        'business.Order',
        on_delete=models.CASCADE,
        related_name='order_messages',
        null=True,
        blank=True,
        help_text="Associated order for order-specific messages"
    )
    
    # Anonymous user tracking (redundant with conversation but useful for direct queries)
    session_id = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        db_index=True,
        help_text="Session ID for anonymous messages"
    )
    
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text="IP address of the message sender (for anonymous users)"
    )
    
    # Message content
    content = models.TextField(default='', help_text="Message text content")
    
    # Message status
    is_read = models.BooleanField(
        default=False,
        help_text="Has the message been read by the recipient"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_message'
        verbose_name = 'User Message'
        verbose_name_plural = 'User Messages'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['user', 'message_type']),
            models.Index(fields=['order', 'message_type']),
            models.Index(fields=['conversation']),
            models.Index(fields=['created_at']),
            models.Index(fields=['session_id']),
        ]
    
    def __str__(self):
        content_preview = self.content[:50] + '...' if len(self.content) > 50 else self.content
        return f"{self.message_type} - {self.sender}: {content_preview}"
    
    @property
    def is_anonymous(self):
        """Check if this is an anonymous message"""
        return self.message_type == 'anonymous' and self.user is None
    
    @property
    def total_attachments_size(self):
        """Get total size of all attachments in bytes"""
        return sum(attachment.file_size for attachment in self.attachments.all())
    
    def save(self, *args, **kwargs):
        """Update conversation's last_message_at on save"""
        super().save(*args, **kwargs)
        if self.conversation:
            self.conversation.last_message_at = self.created_at
            self.conversation.save(update_fields=['last_message_at', 'updated_at'])


class MessageAttachment(models.Model):
    """
    File attachments for Message model (in-system users)
    Allowed: images, PDF, TXT, Word documents
    Max: 5MB per file, 100MB total per message thread
    """
    id = models.CharField(
        max_length=36,
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='attachments'
    )
    
    file = models.FileField(
        upload_to=message_attachment_path,
        validators=[
            validate_attachment_size,
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'pdf', 'txt', 'doc', 'docx']
            )
        ],
        help_text="Allowed: images, PDF, TXT, Word (max 5MB per file)"
    )
    
    original_filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField(help_text="File size in bytes")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'message_attachment'
        verbose_name = 'Message Attachment'
        verbose_name_plural = 'Message Attachments'
        ordering = ['uploaded_at']
    
    def __str__(self):
        return f"{self.original_filename} ({self.file_size} bytes)"
    
    def clean(self):
        """Validate total thread attachment size doesn't exceed 100MB"""
        if self.message:
            validate_thread_total_size(self.message)
    
    def save(self, *args, **kwargs):
        if not self.original_filename and self.file:
            self.original_filename = os.path.basename(self.file.name)
        if not self.file_size and self.file:
            self.file_size = self.file.size
        super().save(*args, **kwargs)
