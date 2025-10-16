# core/models.py
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import datetime
import os

User = get_user_model()


def validate_file_size(value):
    filesize = value.size
    if filesize > 80 * 1024 * 1024:  # 80MB
        raise ValidationError("The maximum file size that can be uploaded is 80MB.")
    else:
        return value


def about_section_media_path(instance, filename):
    """Generate file path for about section media."""
    # file will be uploaded to MEDIA_ROOT/about_section/<id>/<filename>
    return f'about_section/{instance.id}/{filename}'



class NewsletterSubscription(models.Model):
    """
    Stores newsletter subscriber emails
    """
    email = models.EmailField(unique=True)
    date_subscribed = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'newsletter_subscription'
        verbose_name = 'Newsletter Subscription'
        verbose_name_plural = 'Newsletter Subscriptions'
        ordering = ['-date_subscribed']

    def __str__(self):
        return self.email


class ContactInfo(models.Model):
    """
    ContactInfo model for brand/contact/social info
    """
    brand_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=255, blank=True)
    # Social links: dict with keys: ig, git, linkedin, x, reddit
    social_links = models.JSONField(
        blank=True, null=True,
        help_text="JSON object: { 'ig': '...', 'git': '...', 'linkedin': '...', 'x': '...', 'reddit': '...' }"
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'contact_info'
        verbose_name = 'Contact Info'
        verbose_name_plural = 'Contact Info'
        ordering = ['-date_created']

    def __str__(self):
        return self.brand_name


class HeroSection(models.Model):
    """
    Hero section content for homepage
    Should only have one active record at a time
    """
    
    id = models.AutoField(primary_key=True)
    PAGE_CHOICES = [
        ("home", "Home"),
        ("about", "About"),
        ("services", "Services"),
        ("blog", "Blog"),
    ]
    page = models.CharField(max_length=20, choices=PAGE_CHOICES, default="home", help_text="Page this hero section belongs to")
    heading = models.CharField(max_length=255)
    subheading = models.CharField(max_length=500, blank=True)
    cta_text = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Call-to-action button text"
    )
    cta_link = models.TextField(
        blank=True,
        help_text="Call-to-action button URL"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Only one hero section should be active at a time per page"
    )
    
    # Timestamps
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hero_section'
        verbose_name = 'Hero Section'
        verbose_name_plural = 'Hero Sections'
        ordering = ['-date_created']
    
    def __str__(self):
        return self.heading
    
    def save(self, *args, **kwargs):
        """Ensure only one active hero section exists per page"""
        if self.is_active:
            HeroSection.objects.filter(is_active=True, page=self.page).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

# Replace  Work Experience with Team
class WorkExperience(models.Model):
    """
    Work experience entries for about page
    """
    MONTH_CHOICES = [
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
        (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
        (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
    ]
    
    # Basic Info
    company_name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    industry = models.CharField(max_length=100, blank=True)
    company_logo = models.URLField(blank=True, help_text="URL to company logo image")
    company_website = models.URLField(blank=True)
    
    # Duration
    start_month = models.IntegerField(choices=MONTH_CHOICES)
    start_year = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.date.today().year + 10)]
    )
    end_month = models.IntegerField(choices=MONTH_CHOICES, blank=True, null=True)
    end_year = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.date.today().year + 10)],
        blank=True, null=True
    )
    is_current = models.BooleanField(
        default=False, 
        help_text="Check if this is your current position"
    )
    
    # Job Details
    description = models.TextField(help_text="Detailed job description and achievements")
    key_responsibilities = models.JSONField(
        blank=True, null=True,
        help_text="JSON array of key responsibilities: ['Responsibility 1', 'Responsibility 2']"
    )
    achievements = models.JSONField(
        blank=True, null=True,
        help_text="JSON array of key achievements: ['Achievement 1', 'Achievement 2']"
    )
    
    # Technology Stack
    technology_stack = models.JSONField(
        blank=True, null=True,
        help_text="JSON array of technologies used: ['Python', 'Django', 'React']"
    )
    
    # Display Options
    is_featured = models.BooleanField(
        default=True,
        help_text="Display this experience in the main timeline"
    )
    display_order = models.IntegerField(
        default=0,
        help_text="Order of display (0 = first, higher numbers = later)"
    )
    
    # Timestamps
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'work_experience'
        verbose_name = 'Work Experience'
        verbose_name_plural = 'Work Experiences'
        ordering = ['-start_year', '-start_month', 'display_order']
    
    def __str__(self):
        return f"{self.job_title} at {self.company_name}"
    
    @property
    def duration_text(self):
        """Returns formatted duration text"""
        start = f"{self.get_start_month_display()} {self.start_year}"
        if self.is_current:
            return f"{start} — Present"
        elif self.end_month and self.end_year:
            end = f"{self.get_end_month_display()} {self.end_year}"
            return f"{start} — {end}"
        else:
            return start
    
    @property
    def duration_months(self):
        """Calculate total duration in months"""
        if not self.start_year or not self.start_month:
            return None  # or 0, or 1, depending on your preference
        start_date = datetime.date(self.start_year, self.start_month, 1)
        if self.is_current:
            end_date = datetime.date.today()
        elif self.end_year and self.end_month:
            end_date = datetime.date(self.end_year, self.end_month, 1)
        else:
            return 1
        return (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month) + 1


class AboutStats(models.Model):
    """
    Statistics for about page (key-value pairs)
    """
    stat_name = models.CharField(max_length=100)
    stat_value = models.CharField(max_length=50)
    stat_description = models.CharField(max_length=200, blank=True)
    icon_name = models.CharField(
        max_length=50, blank=True,
        help_text="Lucide icon name (e.g., 'users', 'calendar', 'trophy')"
    )
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'about_stats'
        verbose_name = 'About Statistic'
        verbose_name_plural = 'About Statistics'
        ordering = ['display_order', 'stat_name']
    
    def __str__(self):
        return f"{self.stat_name}: {self.stat_value}"


class WhyChooseUs(models.Model):
    """
    Why choose us reasons (key-value pairs)
    """
    reason_title = models.CharField(max_length=200)
    reason_description = models.TextField()
    icon_name = models.CharField(
        max_length=50, blank=True,
        help_text="Lucide icon name (e.g., 'shield', 'zap', 'heart')"
    )
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'why_choose_us'
        verbose_name = 'Why Choose Us'
        verbose_name_plural = 'Why Choose Us'
        ordering = ['display_order', 'reason_title']
    
    def __str__(self):
        return self.reason_title


class Roadmap(models.Model):
    """
    Roadmap milestones (key-value pairs)
    """
    milestone_title = models.CharField(max_length=200)
    milestone_description = models.TextField()
    target_date = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    completion_date = models.DateField(blank=True, null=True)
    icon_name = models.CharField(
        max_length=50, blank=True,
        help_text="Lucide icon name (e.g., 'flag', 'target', 'rocket')"
    )
    
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'roadmap'
        verbose_name = 'Roadmap Milestone'
        verbose_name_plural = 'Roadmap Milestones'
        ordering = ['display_order', 'target_date']
    
    def __str__(self):
        return self.milestone_title


class AboutSection(models.Model):
    """
    About section content for about page
    Should only have one active record at a time
    """
    
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    media = models.FileField(
        upload_to=about_section_media_path,
        blank=True,
        null=True,
        help_text="Upload an image (JPG, JPEG, PNG) or video (MP4, MOV, etc.). Max size: 80MB.",
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'mp4', 'mov', 'avi', 'wmv']),
            validate_file_size
        ]
    )
    socials_urls = models.JSONField(
        blank=True,
        null=True,
        help_text="JSON array of social media links: [{'name': 'twitter', 'url': '...'}]"
    )
    
    # Display Options
    show_stats = models.BooleanField(default=True, help_text="Show statistics section")
    show_work_experience = models.BooleanField(default=True, help_text="Show work experience timeline")
    show_why_choose_us = models.BooleanField(default=True, help_text="Show why choose us section")
    show_roadmap = models.BooleanField(default=False, help_text="Show roadmap section")
    
    # Timestamps
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'about_section'
        verbose_name = 'About Section'
        verbose_name_plural = 'About Sections'
        ordering = ['-date_created']


# Define supported file formats
SUPPORTED_FILE_FORMATS = ['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'gif', 'webp']

def support_attachment_path(instance, filename):
    """Generate file path for support attachments."""
    return f'support_attachments/{instance.ticket.user.id}/{instance.ticket.id}/{filename}'

class SupportTicket(models.Model):
    """Support ticket model for customer inquiries."""
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'), 
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    # Basic fields
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='support_tickets',
        help_text="Client who created this ticket"
    )
    subject = models.CharField(
        max_length=200,
        help_text="Brief description of the issue"
    )
    message = models.TextField(help_text="Detailed description of the issue")
    priority = models.CharField(
        max_length=10, 
        choices=PRIORITY_CHOICES, 
        default='medium'
    )
    status = models.CharField(
        max_length=15, 
        choices=STATUS_CHOICES, 
        default='open'
    )
    
    # Admin response
    admin_reply = models.TextField(
        blank=True, 
        null=True,
        help_text="Admin response to the support ticket"
    )
    admin_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='admin_support_replies',
        help_text="Admin who replied to this ticket"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Support Ticket'
        verbose_name_plural = 'Support Tickets'
    
    def __str__(self):
        return f"Ticket #{self.id} - {self.subject}"
    
    @property
    def messages_count(self):
        """Count of total messages (initial + admin replies)."""
        count = 1  # Initial message
        if self.admin_reply:
            count += 1
        return count
    
    def save(self, *args, **kwargs):
        # Auto-set resolved_at when status changes to resolved
        if self.status == 'resolved' and not self.resolved_at:
            self.resolved_at = timezone.now()
        super().save(*args, **kwargs)


class SupportAttachment(models.Model):
    """File attachments for support tickets."""
    
    ticket = models.ForeignKey(
        SupportTicket,
        on_delete=models.CASCADE,
        related_name='attachments'
    )
    file = models.FileField(
        upload_to=support_attachment_path,
        validators=[
            FileExtensionValidator(allowed_extensions=SUPPORTED_FILE_FORMATS)
        ],
        help_text="Supported formats: PDF, Word docs, and images (JPG, PNG, etc.)"
    )
    original_filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField(help_text="File size in bytes")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['uploaded_at']
        verbose_name = 'Support Attachment'
        verbose_name_plural = 'Support Attachments'
    
    def __str__(self):
        return f"Attachment for Ticket #{self.ticket.id}: {self.original_filename}"
    
    def save(self, *args, **kwargs):
        if self.file:
            self.original_filename = self.file.name
            self.file_size = self.file.size
        super().save(*args, **kwargs)
    
    @property
    def file_extension(self):
        """Get file extension."""
        return os.path.splitext(self.original_filename)[1].lower()
    
    @property
    def is_image(self):
        """Check if attachment is an image."""
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        return self.file_extension in image_extensions
    
    def __str__(self):
        return self.title
    