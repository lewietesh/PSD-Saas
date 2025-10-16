# projects/models.py
import uuid
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
import os


def validate_project_image_size(file):
    """
    Validate project image file size (max 12MB)
    """
    if not file:
        return
    
    max_size = 12 * 1024 * 1024  # 12MB
    if file.size > max_size:
        raise ValidationError(
            f'Image file size must be under 12MB. Current size: {file.size / (1024 * 1024):.2f}MB'
        )


def validate_section_media_file(file):
    """
    Validate media files for project sections:
    - Images: max 5MB
    - Videos: max 50MB
    """
    if not file:
        return
    
    # Get file extension
    ext = os.path.splitext(file.name)[1].lower()
    
    # Define allowed extensions and size limits
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']
    video_extensions = ['.mp4', '.webm', '.ogg', '.mov', '.avi']
    
    if ext in image_extensions:
        # Images: 5MB limit
        max_size = 5 * 1024 * 1024  # 5MB
        if file.size > max_size:
            raise ValidationError(
                f'Image file size must be under 5MB. Current size: {file.size / (1024 * 1024):.2f}MB'
            )
    elif ext in video_extensions:
        # Videos: 50MB limit
        max_size = 50 * 1024 * 1024  # 50MB
        if file.size > max_size:
            raise ValidationError(
                f'Video file size must be under 50MB. Current size: {file.size / (1024 * 1024):.2f}MB'
            )
    else:
        raise ValidationError(
            f'Unsupported file type: {ext}. Allowed: Images (jpg, png, gif, webp, svg) or Videos (mp4, webm, mov)'
        )


class Technology(models.Model):
    """
    Master list of technologies used across projects and products
    Shared reference model
    """
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    icon_url = models.TextField(blank=True)
    category = models.CharField(
        max_length=50, 
        blank=True,
        help_text="Category: frontend, backend, database, tool, etc."
    )
    
    class Meta:
        db_table = 'technology'
        verbose_name = 'Technology'
        verbose_name_plural = 'Technologies'
        ordering = ['category', 'name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return self.name


class Project(models.Model):
    """
    Portfolio projects showcasing development work
    """
    
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('maintenance', 'Maintenance'),
    ]
    
    # Primary fields
    id = models.CharField(
        max_length=36, 
        primary_key=True, 
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    
    # Categorization
    category = models.CharField(max_length=100, blank=True)
    domain = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Business domain or industry"
    )
    
    # Relationships
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='client_projects',
        limit_choices_to={'role': 'client'}
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='authored_projects',
        help_text="Internal team member responsible for the project"
    )
    
    # Media
    image = models.ImageField(
        upload_to='projects/featured/',
        blank=True,
        null=True,
        help_text="Main project screenshot or banner (JPG, JPEG, PNG, WEBP - Max 12MB)",
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp']),
            validate_project_image_size
        ]
    )
    
    # Project sections for showcase
    sections = models.JSONField(
        default=list,
        blank=True,
        help_text="Project sections with section_id, media_url, and description for detailed showcase"
    )
    
    # Content fields
    description = models.TextField()
    content = models.TextField(
        blank=True,
        help_text="Detailed project content and case study"
    )
    
    # Project links
    url = models.TextField(
        blank=True,
        help_text="Live project URL"
    )
    repository_url = models.TextField(
        blank=True,
        help_text="GitHub or code repository URL"
    )
    
    # Project metrics
    likes = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    
    # Project timeline
    completion_date = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ongoing'
    )
    
    # Technology relationship
    technologies = models.ManyToManyField(
        Technology,
        through='ProjectTechnology',
        related_name='projects',
        blank=True
    )
    
    # Timestamps
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'project'
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['-date_created']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
            models.Index(fields=['featured']),
            models.Index(fields=['client']),
            models.Index(fields=['author']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """Auto-generate slug from title if not provided"""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def is_completed(self):
        """Check if project is completed"""
        return self.status == 'completed'


class ProjectGalleryImage(models.Model):
    """
    Gallery images for projects (multiple screenshots)
    """
    
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='gallery_images'
    )
    image = models.ImageField(
        upload_to='projects/gallery/',
        blank=True,
        null=True,
        help_text="Gallery image (JPG, JPEG, PNG, WEBP - Max 12MB)",
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp']),
            validate_project_image_size
        ]
    )
    alt_text = models.CharField(
        max_length=255, 
        blank=True,
        help_text="Alternative text for accessibility"
    )
    sort_order = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'project_gallery_image'
        verbose_name = 'Project Gallery Image'
        verbose_name_plural = 'Project Gallery Images'
        ordering = ['project', 'sort_order']
        indexes = [
            models.Index(fields=['project']),
        ]
    
    def __str__(self):
        return f"{self.project.title} - Image {self.sort_order}"


def validate_section_image_size(file):
    """
    Validate project section image file size (max 10MB)
    """
    if not file:
        return
    
    max_size = 10 * 1024 * 1024  # 10MB
    if file.size > max_size:
        raise ValidationError(
            f'Section image file size must be under 10MB. Current size: {file.size / (1024 * 1024):.2f}MB'
        )


class ProjectSection(models.Model):
    """
    Individual sections for detailed project showcase
    Replaces the JSONField sections with a proper relational model
    """
    
    SECTION_TYPE_CHOICES = [
        ('overview', 'Overview'),
        ('features', 'Features'),
        ('architecture', 'Architecture'),
        ('tech-stack', 'Tech Stack'),
        ('challenge', 'Challenge'),
        ('solution', 'Solution'),
        ('results', 'Results'),
        ('design', 'Design Process'),
        ('development', 'Development'),
        ('testimonial', 'Testimonial'),
        ('other', 'Other'),
    ]
    
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='project_sections'
    )
    section_id = models.CharField(
        max_length=50,
        choices=SECTION_TYPE_CHOICES,
        default='other',
        help_text="Type/identifier for this section"
    )
    section_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Custom section name (optional, defaults to section_id)"
    )
    media = models.ImageField(
        upload_to='projects/sections/',
        blank=True,
        null=True,
        help_text="Section image (JPG, JPEG, PNG, WEBP - Max 10MB)",
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp']),
            validate_section_image_size
        ]
    )
    description = models.TextField(
        help_text="Detailed description for this section"
    )
    sort_order = models.IntegerField(
        default=0,
        help_text="Order in which sections appear (lower numbers first)"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this section is visible"
    )
    date_created = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'project_section'
        verbose_name = 'Project Section'
        verbose_name_plural = 'Project Sections'
        ordering = ['project', 'sort_order']
        indexes = [
            models.Index(fields=['project']),
            models.Index(fields=['sort_order']),
        ]
    
    def __str__(self):
        name = self.section_name or self.get_section_id_display()
        return f"{self.project.title} - {name}"


class ProjectTechnology(models.Model):
    """
    Many-to-many relationship between Project and Technology
    """
    
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )
    technology = models.ForeignKey(
        Technology,
        on_delete=models.CASCADE
    )
    
    class Meta:
        db_table = 'project_technology'
        unique_together = ('project', 'technology')
        verbose_name = 'Project Technology'
        verbose_name_plural = 'Project Technologies'
    
    def __str__(self):
        return f"{self.project.title} - {self.technology.name}"


class ProjectComment(models.Model):
    """
    Public comments on portfolio projects
    """
    
    # Primary fields
    id = models.CharField(
        max_length=36, 
        primary_key=True, 
        default=uuid.uuid4,
        editable=False
    )
    
    # Relationship
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    
    # Commenter information
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    
    # Comment content
    message = models.TextField()
    
    # Moderation
    approved = models.BooleanField(default=False)
    
    # Timestamp
    date_created = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'project_comment'
        verbose_name = 'Project Comment'
        verbose_name_plural = 'Project Comments'
        ordering = ['-date_created']
        indexes = [
            models.Index(fields=['project']),
            models.Index(fields=['approved']),
        ]
    
    def __str__(self):
        return f"Comment by {self.name} on {self.project.title}"