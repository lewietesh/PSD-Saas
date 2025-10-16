
# business/models.py
# Standard library imports
import os
import uuid


# Django imports
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError


# ServiceRequest model for anonymous or authenticated service leads
class ServiceRequest(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('technical', 'Technical'),
        ('writing', 'Writing'),
    ]
    # File upload (optional, 15MB limit, allowed types)
    attachment = models.FileField(
        upload_to='service_requests/',
        blank=True,
        null=True,
        help_text="Optional file upload (max 15MB, pdf/doc/docx/txt/jpg/png/zip)"
    )

    def clean(self):
        super().clean()
        if self.attachment:
            # Validate file size (max 15MB)
            if self.attachment.size > 15 * 1024 * 1024:
                raise ValidationError('Attachment file size must be under 15MB.')
            # Validate file type
            ext = os.path.splitext(self.attachment.name)[1].lower()
            allowed = ['.pdf', '.doc', '.docx', '.txt', '.jpg', '.jpeg', '.png', '.zip']
            if ext not in allowed:
                raise ValidationError('Invalid file type. Allowed: pdf, doc, docx, txt, jpg, jpeg, png, zip.')
    """
    Lightweight service request for lead capture and conversion funnel.
    Can be linked to zero or one Order.
    """
    id = models.CharField(
        max_length=36,
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    service = models.ForeignKey(
        'services.Service',
        on_delete=models.CASCADE,
        related_name='requests'
    )
    pricing_tier = models.ForeignKey(
        'services.ServicePricingTier',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='service_requests'
    )
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    project_description = models.TextField()
    budget = models.CharField(max_length=50, blank=True)
    timeline = models.CharField(max_length=100, blank=True)
    service_type = models.CharField(
        max_length=20,
        choices=SERVICE_TYPE_CHOICES,
        default='technical'
    )
    subject = models.CharField(max_length=255, blank=True)
    citations = models.CharField(max_length=255, blank=True)
    formatting_style = models.CharField(max_length=100, blank=True)
    pages = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('new', 'New'),
            ('contacted', 'Contacted'),
            ('converted', 'Converted'),
            ('rejected', 'Rejected'),
        ],
        default='new'
    )
    order = models.OneToOneField(
        'business.Order',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='service_request',
        help_text="Order derived from this service request (if converted)"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'service_request'
        verbose_name = 'Service Request'
        verbose_name_plural = 'Service Requests'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.service.name} request from {self.email}"


class Order(models.Model):
    """
    Orders for services or products
    Links clients to their purchases
    """
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    # Primary fields
    id = models.CharField(
        max_length=36, 
        primary_key=True, 
        default=uuid.uuid4,
        editable=False
    )
    
    # Relationships
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_orders',
        limit_choices_to={'role': 'client'}
    )
    service = models.ForeignKey(
        'services.Service',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    pricing_tier = models.ForeignKey(
        'services.ServicePricingTier',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    
    # Financial fields
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='KSH')
    
    # Status fields
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )
    
    # Payment information
    payment_method = models.CharField(max_length=50, blank=True)
    transaction_id = models.CharField(max_length=255, blank=True)
    
    # Additional fields
    notes = models.TextField(blank=True)
    due_date = models.DateField(blank=True, null=True)
    
    # File attachments - stored as arrays of filenames
    attachments = models.JSONField(
        default=list,
        blank=True,
        help_text="Array of attachment filenames uploaded by client"
    )
    work_results = models.JSONField(
        default=list,
        blank=True,
        help_text="Array of work result filenames uploaded by admin/contractor"
    )
    
    # Timestamps
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'order'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-date_created']
        indexes = [
            models.Index(fields=['client']),
            models.Index(fields=['status']),
            models.Index(fields=['payment_status']),
        ]
    
    def __str__(self):
        return f"Order {self.id[:8]} - {self.client.email}"
    
    def add_attachment(self, filename):
        """Add a filename to the attachments array"""
        if filename not in self.attachments:
            self.attachments.append(filename)
            self.save(update_fields=['attachments'])
    
    def remove_attachment(self, filename):
        """Remove a filename from the attachments array"""
        if filename in self.attachments:
            self.attachments.remove(filename)
            self.save(update_fields=['attachments'])
    
    def add_work_result(self, filename):
        """Add a filename to the work_results array"""
        if filename not in self.work_results:
            self.work_results.append(filename)
            self.save(update_fields=['work_results'])
    
    def remove_work_result(self, filename):
        """Remove a filename from the work_results array"""
        if filename in self.work_results:
            self.work_results.remove(filename)
            self.save(update_fields=['work_results'])
    
    def get_attachment_paths(self):
        """Get full paths for all attachment files"""
        return [os.path.join(settings.MEDIA_ROOT, 'orders', 'attachments', filename) 
                for filename in self.attachments]
    
    def get_work_result_paths(self):
        """Get full paths for all work result files"""

        return [os.path.join(settings.MEDIA_ROOT, 'orders', 'work_results', filename) 
                for filename in self.work_results]


class Testimonial(models.Model):
    """
    Client testimonials for social proof
    """
    
    # Primary fields
    id = models.CharField(
        max_length=36, 
        primary_key=True, 
        default=uuid.uuid4,
        editable=False
    )
    
    # Relationships
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_testimonials',
        limit_choices_to={'role': 'client'}
    )
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='testimonials',
        help_text="Link to specific project if applicable"
    )
    service = models.ForeignKey(
        'services.Service',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='testimonials',
        help_text="Link to specific service if applicable"
    )
    
    # Content fields
    content = models.TextField()
    rating = models.IntegerField(
        blank=True,
        null=True,
        help_text="Rating from 1-5"
    )
    
    # Moderation fields
    featured = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    
    # Timestamp
    date_created = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'testimonial'
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'
        ordering = ['-date_created']
        indexes = [
            models.Index(fields=['client']),
            models.Index(fields=['featured']),
            models.Index(fields=['approved']),
        ]
    
    def __str__(self):
        return f"Testimonial by {self.client.email}"


class Notification(models.Model):
    """
    System notifications for admin users
    """
    
    TYPE_CHOICES = [
        ('order', 'Order'),
        ('contact', 'Contact'),
        ('system', 'System'),
        ('payment', 'Payment'),
        ('review', 'Review'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Primary fields
    id = models.CharField(
        max_length=36, 
        primary_key=True, 
        default=uuid.uuid4,
        editable=False
    )
    
    # Relationships
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    
    # Content fields
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    
    # Status fields
    is_read = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    
    # Generic relationship fields
    resource_id = models.CharField(max_length=36, blank=True)
    resource_type = models.CharField(max_length=50, blank=True)
    
    # Timestamp
    date_created = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'notification'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-date_created']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['is_read']),
            models.Index(fields=['type']),
            models.Index(fields=['priority']),
        ]
    
    def __str__(self):
        return f"{self.type.title()} notification: {self.title}"


class ContactMessage(models.Model):
    """
    Contact form submissions for lead capture
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

class Payment(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default='pending')  # pending, completed, failed, refunded
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'payment'
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.order_id} - {self.status}"


class PayPalPayment(models.Model):
    """
    PayPal specific payment details linked to a Payment record
    """
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='paypal_details')
    paypal_order_id = models.CharField(max_length=255)
    paypal_payer_id = models.CharField(max_length=255, blank=True, null=True)
    paypal_payer_email = models.EmailField(blank=True, null=True)
    paypal_payment_id = models.CharField(max_length=255, blank=True, null=True)
    paypal_status = models.CharField(max_length=50, default='CREATED')
    paypal_intent = models.CharField(max_length=20, default='CAPTURE')
    paypal_create_time = models.DateTimeField(null=True, blank=True)
    paypal_update_time = models.DateTimeField(null=True, blank=True)
    paypal_data = models.TextField(blank=True, null=True)  # JSON data as text
    is_balance_deposit = models.BooleanField(default=False)  # Flag for account balance deposits

    class Meta:
        db_table = 'paypal_payment'
        verbose_name = 'PayPal Payment'
        verbose_name_plural = 'PayPal Payments'
    
    def __str__(self):
        return f"PayPal: {self.paypal_order_id}"


## AccountBalance model removed; balance tracked on accounts.User
