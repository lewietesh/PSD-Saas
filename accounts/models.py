# accounts/models.py
import uuid
import mimetypes
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone


# Signal to automatically create ClientProfile for client users
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email and password"""
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email and password"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model for system authentication
    Supports three user types: developers, admin, and clients
    """
    
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('partner', 'Partner'),
        ('client', 'Client'),
    ]
    
    # Primary fields
    id = models.CharField(
        max_length=36, 
        primary_key=True, 
        default=uuid.uuid4,
        editable=False
    )
    email = models.EmailField(unique=True)
    
    # Personal information
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    profile_img = models.ImageField(upload_to='profile_images/', blank=True, null=True, help_text="Profile image (Google or uploaded)")
    
    # Contact information
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(
        validators=[phone_regex], 
        max_length=20, 
        blank=True
    )
    
    # Role and permissions
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='client'
    )
    
    # Verification and permissions
    is_verified = models.BooleanField(default=False, help_text="Has the user's email been verified?")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    two_factor_enabled = models.BooleanField(default=False, help_text="Is two-factor authentication enabled for this user?")
    is_social_login = models.BooleanField(default=False, help_text="User authenticated via social login (Google, etc.)")
    affiliate_code = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        unique=True,
        help_text="Optional affiliate/referral code for partner tracking"
    )
    
    # Preferences and account fields
    account_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text="Denormalized user balance for quick reads")
    currency = models.CharField(max_length=10, default='USD', blank=True, help_text="Preferred currency code (e.g., USD, KSH)")
    language_preference = models.CharField(max_length=32, default='English', blank=True, help_text="Preferred language name (e.g., English)")
    user_timezone = models.CharField(
        max_length=50, 
        default='GMT', 
        blank=True,
        help_text="User's timezone (e.g., GMT, America/New_York, Africa/Nairobi)"
    )

    # Timestamps
    date_joined = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    
    # Manager and authentication
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        db_table = 'auth_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        """Return the user's full name"""
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def can_change_password(self):
        """Return True if user can change their password (not a social login user)"""
        return not self.is_social_login and self.has_usable_password()
    
    def save(self, *args, **kwargs):
        """Override save to set staff status and superuser based on role"""
        if self.role == 'admin':
            self.is_staff = True
            self.is_superuser = True
        elif self.role == 'partner':
            self.is_staff = True
            self.is_superuser = False
        else:
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)


class ClientProfile(models.Model):
    """
    Extended profile for users with 'client' role
    Contains essential business information for external customers
    """
    
    # One-to-One relationship with User
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='client_profile'
    )
    
    # Essential business fields
    company_name = models.CharField(max_length=255, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    
    # Financial tracking
    account_balance = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0.00
    )
    
    # Timestamps
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'client'
        verbose_name = 'Client Profile'
        verbose_name_plural = 'Client Profiles'
        ordering = ['-date_created']
    
    def __str__(self):
        return self.company_name or self.user.full_name


# Signal to automatically create ClientProfile for client users
@receiver(post_save, sender=User)
def create_client_profile(sender, instance, created, **kwargs):
    """Automatically create ClientProfile when User with role 'client' is created"""
    if instance.role == 'client':
        ClientProfile.objects.get_or_create(user=instance)


MAX_PARTNER_VIDEO_SIZE = 64 * 1024 * 1024  # 64 MB
IMAGE_MIME_TYPES = {
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/webp',
    'image/svg+xml',
}
VIDEO_MIME_TYPES = {
    'video/mp4',
    'video/quicktime',
    'video/webm',
    'video/x-matroska',
}


def validate_partner_media(file):
    """Validate uploaded partner media to ensure it's an image or acceptable video under 64MB."""
    mime_type, _ = mimetypes.guess_type(file.name)
    content_type = getattr(file, 'content_type', None) or mime_type

    if not content_type:
        raise ValidationError('Unable to determine file type. Upload an image or video file.')

    if content_type in IMAGE_MIME_TYPES:
        return

    if content_type in VIDEO_MIME_TYPES:
        file_size = getattr(file, 'size', None)
        if file_size and file_size > MAX_PARTNER_VIDEO_SIZE:
            raise ValidationError('Video files must be 64MB or smaller.')
        return

    raise ValidationError('Media must be an image or one of the supported video formats (MP4, MOV, WEBM, MKV).')


class Partner(models.Model):
    """Branded partner profile linked to an admin-level user."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='partner_profile'
    )
    professional_title = models.CharField(max_length=150, blank=True)
    domain = models.CharField(
        max_length=120,
        blank=True,
        help_text="Primary domain or industry focus"
    )
    professional_summary = models.TextField(blank=True)
    website = models.URLField(blank=True)
    social_urls = models.JSONField(
        default=list,
        blank=True,
        null=True,
        help_text="List of social media profiles as objects: [{'name': 'linkedin', 'url': 'https://...'}]"
    )
    affiliate_clients = models.JSONField(default=list, blank=True, null=True)
    media_url = models.FileField(
        upload_to='partners/media/',
        blank=True,
        null=True,
        validators=[validate_partner_media]
    )
    # NOTE: These JSONFields are placeholders for lightweight denormalized associations.
    # Planned refactor: replace with proper FK/M2M relationships and expose only ID arrays
    # to the frontend (e.g., services_ids, project_ids) for clarity & integrity.
    # This preserves current behavior until related domain models are finalized.
    def _validate_id_list(value):  # type: ignore
        """Ensure JSONField holds a list of string IDs (UUIDs or PKs).

        Accepts empty / None -> coerced to empty list during serializer usage.
        We don't strictly validate UUID format here to allow future non-UUID PKs,
        but we enforce string type to avoid accidental object dumps.
        """
        if value in (None, ""):
            return []
        if not isinstance(value, list):
            raise ValidationError('Value must be a list of ID strings.')
        cleaned = []
        for idx, item in enumerate(value):
            if isinstance(item, str):
                item_clean = item.strip()
                if not item_clean:
                    continue
                cleaned.append(item_clean)
            else:
                raise ValidationError(f'Entry at index {idx} is not a string ID.')
        return cleaned

    services = models.JSONField(
        default=list,
        blank=True,
        null=True,
        validators=[_validate_id_list],
        help_text="Array of Service IDs (read-only exposure on public API)."
    )
    orders = models.JSONField(
        default=list,
        blank=True,
        null=True,
        validators=[_validate_id_list],
        help_text="Array of Order IDs (may reference client orders)."
    )
    blog_posts = models.JSONField(
        default=list,
        blank=True,
        null=True,
        validators=[_validate_id_list],
        help_text="Array of BlogPost IDs authored or associated with this partner."
    )
    projects = models.JSONField(
        default=list,
        blank=True,
        null=True,
        validators=[_validate_id_list],
        help_text="Array of Project IDs linked to this partner."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.full_name or self.user.email} Partner Profile"

    def save(self, *args, **kwargs):
        # Ensure linked user has partner privileges
        if self.user.role != 'partner':
            self.user.role = 'partner'
        if not self.user.is_staff:
            self.user.is_staff = True
        self.user.save(update_fields=['role', 'is_staff'])
        super().save(*args, **kwargs)

