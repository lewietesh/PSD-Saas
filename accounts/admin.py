# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import PermissionDenied
from django.utils.html import format_html
from django import forms
from .models import User, ClientProfile, Partner, MAX_PARTNER_VIDEO_SIZE


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form with role and email"""
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'role', 'affiliate_code')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove username field since we use email
        if 'username' in self.fields:
            del self.fields['username']
    
    def save(self, commit=True):
        """Save user with properly hashed password"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        
        # Set is_staff and is_superuser based on role
        if user.role == 'admin':
            user.is_staff = True
            user.is_superuser = True
        elif user.role == 'partner':
            user.is_staff = True
            user.is_superuser = False
        else:
            user.is_staff = False
            user.is_superuser = False
            
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    """Custom user change form"""
    
    class Meta:
        model = User
        fields = '__all__'


# Base Admin Mixin for all models
class BaseAdminPermissions(admin.ModelAdmin):
    """
    Base admin class with common permission patterns for all models.
    All admin classes should inherit from this to ensure Partners have access.
    """
    
    def has_module_permission(self, request):
        """Check if user has permission to access this admin module"""
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        elif hasattr(request.user, 'role') and request.user.role in ['admin', 'partner']:
            return True
        return False
    
    def has_view_permission(self, request, obj=None):
        """Allow partners to view objects"""
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        elif hasattr(request.user, 'role') and request.user.role in ['admin', 'partner']:
            return True
        return False
    
    def has_add_permission(self, request):
        """Allow partners to add objects"""
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        elif hasattr(request.user, 'role') and request.user.role in ['admin', 'partner']:
            return True
        return False
    
    def has_change_permission(self, request, obj=None):
        """Allow partners to change objects"""
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        elif hasattr(request.user, 'role') and request.user.role in ['admin', 'partner']:
            return True
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Allow partners to delete objects"""
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        elif hasattr(request.user, 'role') and request.user.role in ['admin', 'partner']:
            return True
        return False


class ClientProfileInline(admin.StackedInline):
    """Inline client profile for user admin"""
    model = ClientProfile
    can_delete = False
    verbose_name_plural = 'Client Profile'
    readonly_fields = ('date_created', 'date_updated')
    
    def has_add_permission(self, request, obj=None):
        """Only show for client users"""
        if obj and obj.role == 'client':
            return True
        return False
    
    def has_change_permission(self, request, obj=None):
        """Allow editing client profiles"""
        if obj and obj.role == 'client':
            return True
        return False


class PartnerAdminForm(forms.ModelForm):
    """Admin form for partner profile with media validation and friendly social inputs."""

    # Include GitHub again per updated requirement
    SOCIAL_PLATFORMS = (
        ('linkedin', 'LinkedIn'),
        ('x', 'X / Twitter'),
        ('github', 'GitHub'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
    )

    social_linkedin = forms.URLField(label='LinkedIn', required=False)
    social_x = forms.URLField(label='X / Twitter', required=False)
    social_github = forms.URLField(label='GitHub', required=False)
    social_instagram = forms.URLField(label='Instagram', required=False)
    social_youtube = forms.URLField(label='YouTube', required=False)

    class Meta:
        model = Partner
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        # IMPORTANT: pass args/kwargs to parent so fields are initialized
        super().__init__(*args, **kwargs)
        # Guard in case migrations not applied or field excluded
        social_field = self.fields.get('social_urls')
        if social_field:
            social_field.required = False
            social_field.widget = forms.HiddenInput()
        else:
            # Soft fail: avoid KeyError while still allowing admin to load
            # You can remove this branch once confirmed migrations are applied.
            pass

        existing = {}
        self._extra_social_entries = []
        social_data = self.instance.social_urls if getattr(self.instance, 'social_urls', None) else []
        if isinstance(social_data, dict):
            existing = social_data
        elif isinstance(social_data, list):
            for entry in social_data:
                if isinstance(entry, dict) and 'name' in entry and 'url' in entry:
                    key = entry['name']
                    if key in dict(self.SOCIAL_PLATFORMS):
                        existing[key] = entry['url']
                    else:
                        self._extra_social_entries.append(entry)

        for key, _label in self.SOCIAL_PLATFORMS:
            field_name = f'social_{key}'
            if field_name in self.fields:
                self.fields[field_name].initial = existing.get(key)

    def clean_media_url(self):
        media = self.cleaned_data.get('media_url')
        if not media:
            return media

        content_type = getattr(media, 'content_type', '')
        if content_type.startswith('video/') and media.size > MAX_PARTNER_VIDEO_SIZE:
            raise forms.ValidationError('Video files must be 64MB or smaller.')
        return media

    def clean(self):
        cleaned = super().clean()
        social_urls = []
        for key, label in self.SOCIAL_PLATFORMS:
            url = cleaned.get(f'social_{key}')
            if url:
                social_urls.append({'name': key, 'url': url})
        social_urls.extend(getattr(self, '_extra_social_entries', []))
        cleaned['social_urls'] = social_urls
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.social_urls = self.cleaned_data.get('social_urls', [])
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class PartnerInline(admin.StackedInline):
    """Inline partner profile for admin users."""

    model = Partner
    form = PartnerAdminForm
    can_delete = True
    verbose_name_plural = 'Partner Profile'
    extra = 0
    fieldsets = (
        (None, {
            'fields': (
                'professional_title',
                'domain',
                'professional_summary',
                'website',
                'social_linkedin',
                'social_x',
                'social_github',
                'social_instagram',
                'social_youtube',
                'social_urls',
                'media_url',
            )
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    # Association ID arrays hidden entirely in inline
    exclude = ('affiliate_clients', 'services', 'orders', 'blog_posts', 'projects')
    readonly_fields = ('created_at', 'updated_at')

    def has_add_permission(self, request, obj=None):
        if not obj:
            return False
        return not hasattr(obj, 'partner_profile')

    def has_change_permission(self, request, obj=None):
        if not obj:
            return False
        return hasattr(obj, 'partner_profile')


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom user admin with role-based permissions"""
    
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    
    # Display settings
    list_display = [
        'email', 'full_name_display', 'role', 'affiliate_code', 'is_active', 
        'is_staff', 'date_joined', 'last_login'
    ]
    list_filter = ['role', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name', 'phone', 'affiliate_code']
    ordering = ['-date_joined']
    
    # Detail view settings
    readonly_fields = ['date_joined', 'date_updated', 'last_login']
    
    # Fieldsets for change form
    fieldsets = [
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'phone', 'affiliate_code')
        }),
        ('Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser'),
            'classes': ['collapse']
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined', 'date_updated'),
            'classes': ['collapse']
        }),
    ]
    
    # Fieldsets for add form
    add_fieldsets = [
        (None, {
            'classes': ['wide'],
            'fields': ('email', 'first_name', 'last_name', 'role', 'affiliate_code', 'password1', 'password2'),
        }),
    ]
    
    # Inline for client profiles
    inlines = [ClientProfileInline, PartnerInline]
    
    def full_name_display(self, obj):
        """Display full name with fallback"""
        return obj.full_name or obj.email
    full_name_display.short_description = 'Full Name'
    
    def get_queryset(self, request):
        """Filter queryset based on user role"""
        queryset = super().get_queryset(request)
        
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return queryset.none()
        
        if request.user.is_superuser:
            return queryset
        elif hasattr(request.user, 'role') and request.user.role == 'admin':
            return queryset
        elif hasattr(request.user, 'role') and request.user.role == 'partner':
            # Partners can see all users but not superusers
            return queryset.filter(is_superuser=False)
        else:
            # Clients can only see themselves
            return queryset.filter(id=request.user.id)
    
    def has_add_permission(self, request):
        """Control who can add users"""
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        elif hasattr(request.user, 'role') and request.user.role in ['admin', 'partner']:
            return True
        return False
    
    def has_change_permission(self, request, obj=None):
        """Control who can change users"""
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        elif hasattr(request.user, 'role') and request.user.role == 'admin':
            return True
        elif hasattr(request.user, 'role') and request.user.role == 'partner':
            # Partners can edit non-superusers
            if obj and obj.is_superuser:
                return False
            return True
        elif obj:
            # Users can only edit themselves
            return obj == request.user
        return True
    
    def has_delete_permission(self, request, obj=None):
        """Control who can delete users"""
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        elif hasattr(request.user, 'role') and request.user.role == 'admin':
            # Admins can't delete superusers
            if obj and obj.is_superuser:
                return False
            return True
        elif hasattr(request.user, 'role') and request.user.role == 'partner':
            # Partners can only delete clients
            if obj and hasattr(obj, 'role') and obj.role == 'client':
                return True
            return False
        return False
    
    def get_readonly_fields(self, request, obj=None):
        """Set readonly fields based on permissions"""
        readonly_fields = list(self.readonly_fields)
        
        if not request.user.is_authenticated:
            return readonly_fields
        
        if not request.user.is_superuser:
            if hasattr(request.user, 'role') and request.user.role == 'partner':
                # Partners can't change admin/superuser permissions
                if obj and ((hasattr(obj, 'role') and obj.role in ['admin']) or obj.is_superuser):
                    readonly_fields.extend(['role', 'is_staff', 'is_superuser'])
            elif hasattr(request.user, 'role') and request.user.role == 'admin':
                # Admins can't change superuser status
                readonly_fields.append('is_superuser')
            else:
                # Regular users can't change permissions
                readonly_fields.extend(['role', 'is_staff', 'is_superuser', 'is_active'])
        
        return readonly_fields
    
    def save_model(self, request, obj, form, change):
        """Custom save logic with permission enforcement"""
        if not change:  # New user
            # Ensure proper role assignment
            if obj.role == 'admin':
                obj.is_staff = True
                obj.is_superuser = True
            elif obj.role == 'partner':
                obj.is_staff = True
                obj.is_superuser = False
            else:
                obj.is_staff = False
                obj.is_superuser = False
        
        # Prevent privilege escalation
        if not request.user.is_superuser:
            if hasattr(request.user, 'role') and request.user.role == 'partner':
                # Partners can't create admins or superusers
                if hasattr(obj, 'role') and obj.role == 'admin' or obj.is_superuser:
                    raise PermissionDenied("You don't have permission to create admin users.")
            elif not hasattr(request.user, 'role') or request.user.role != 'admin':
                # Non-admins can't change roles
                if change and 'role' in form.changed_data:
                    raise PermissionDenied("You don't have permission to change user roles.")
        
        super().save_model(request, obj, form, change)


@admin.register(ClientProfile)
class ClientProfileAdmin(BaseAdminPermissions):
    """Client profile admin with business focus"""
    
    list_display = [
        'user_email', 'company_name', 'industry', 
        'formatted_balance', 'date_created'
    ]
    list_filter = ['industry', 'date_created']
    search_fields = [
        'user__email', 'user__first_name', 'user__last_name', 
        'company_name', 'industry'
    ]
    readonly_fields = ['user', 'date_created', 'date_updated']
    
    fieldsets = [
        ('User Information', {
            'fields': ('user',)
        }),
        ('Business Information', {
            'fields': ('company_name', 'industry')
        }),
        ('Financial Information', {
            'fields': ('account_balance',),
            'description': 'Client account balance and financial tracking'
        }),
        ('Timestamps', {
            'fields': ('date_created', 'date_updated'),
            'classes': ['collapse']
        }),
    ]
    
    def user_email(self, obj):
        """Display user email"""
        return obj.user.email
    user_email.short_description = 'Email'
    user_email.admin_order_field = 'user__email'
    
    def formatted_balance(self, obj):
        """Display formatted account balance"""
        balance = obj.account_balance
        color = 'green' if balance > 0 else 'red' if balance < 0 else 'black'
        
        # FIXED: Format the number first, then pass to format_html
        formatted_amount = f"{balance:,.2f}"
        
        return format_html(
            '<span style="color: {};">KSH {}</span>',
            color, formatted_amount
        )
    formatted_balance.short_description = 'Account Balance'
    formatted_balance.admin_order_field = 'account_balance'
    
    def get_queryset(self, request):
        """Filter queryset based on user role"""
        queryset = super().get_queryset(request)
        
        if not request.user.is_authenticated:
            return queryset.none()
        
        if request.user.is_superuser or (hasattr(request.user, 'role') and request.user.role in ['admin', 'partner']):
            return queryset
        elif hasattr(request.user, 'role') and request.user.role == 'client':
            # Clients can only see their own profile
            return queryset.filter(user=request.user)
        return queryset.none()
    
    def has_add_permission(self, request):
        """Control who can add client profiles"""
        # Profiles are auto-created, so no manual addition needed
        return False
    
    def has_change_permission(self, request, obj=None):
        """Control who can change client profiles"""
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser or (hasattr(request.user, 'role') and request.user.role in ['admin', 'partner']):
            return True
        elif obj and hasattr(request.user, 'role') and request.user.role == 'client':
            # Clients can only edit their own profile
            return obj.user == request.user
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Control who can delete client profiles"""
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser or (hasattr(request.user, 'role') and request.user.role == 'admin'):
            return True
        return False
    
    def get_readonly_fields(self, request, obj=None):
        """Set readonly fields based on permissions"""
        readonly_fields = list(self.readonly_fields)
        
        if not request.user.is_authenticated:
            return readonly_fields
        
        if hasattr(request.user, 'role') and request.user.role == 'client':
            # Clients can't change their account balance
            if 'account_balance' not in readonly_fields:
                readonly_fields.append('account_balance')
        
        return readonly_fields


# Custom admin site configuration
admin.site.site_header = 'Portfolio API Administration'
admin.site.site_title = 'Portfolio API Admin'
admin.site.index_title = 'Welcome to Portfolio API Administration'


# Additional admin customizations  
class AdminPermissionMixin:
    """Mixin for common admin permission patterns (deprecated - use BaseAdminPermissions)"""
    
    def has_module_permission(self, request):
        """Check if user has permission to access this admin module"""
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        elif hasattr(request.user, 'role') and request.user.role in ['admin', 'partner']:
            return True
        return False


# Apply the mixin to existing admin classes
UserAdmin.__bases__ = (AdminPermissionMixin, BaseUserAdmin)
ClientProfileAdmin.__bases__ = (AdminPermissionMixin, admin.ModelAdmin)


@admin.register(Partner)
class PartnerAdmin(BaseAdminPermissions):
    """Standalone admin for partner profiles."""

    form = PartnerAdminForm
    list_display = ('user', 'professional_title', 'domain', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'professional_title', 'domain')
    list_filter = ('domain', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    exclude = ('affiliate_clients', 'services', 'orders', 'blog_posts', 'projects')

    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Professional Details', {
            'fields': (
                'professional_title', 'domain', 'professional_summary', 'website',
                'social_linkedin', 'social_x', 'social_github', 'social_instagram', 'social_youtube', 'social_urls',
                'media_url'
            )
        }),
        # Associations removed from admin UI per requirement
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')