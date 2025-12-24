# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User, ClientProfile, Partner


class UserBasicSerializer(serializers.ModelSerializer):
    """
    Basic user information for public display
    """
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name', 'role', 'profile_img', 'is_verified']


class PartnerSerializer(serializers.ModelSerializer):
    """Serializer for partner profiles."""

    social_urls = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField(allow_blank=True),
        ),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Partner
        fields = [
            'professional_title',
            'domain',
            'professional_summary',
            'website',
            'social_urls',
            'media_url',
            'affiliate_clients',
            'services',
            'orders',
            'blog_posts',
            'projects',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_social_urls(self, value):
        if not value:
            return []

        cleaned = []
        for entry in value:
            if not isinstance(entry, dict):
                raise serializers.ValidationError('Each social link must be an object with "name" and "url" keys.')

            name = entry.get('name')
            url = entry.get('url')
            if not name or not url:
                raise serializers.ValidationError('Each social link requires both "name" and "url" values.')
            cleaned.append({'name': name, 'url': url})
        return cleaned


class PartnerPublicSerializer(serializers.ModelSerializer):
    """Slim serializer for public team/partner listings."""

    full_name = serializers.SerializerMethodField()
    email = serializers.EmailField(source='user.email', read_only=True)
    avatar_url = serializers.SerializerMethodField()
    media_url = serializers.SerializerMethodField()
    social_urls = serializers.SerializerMethodField()
    services = serializers.SerializerMethodField()
    affiliate_clients = serializers.SerializerMethodField()
    orders = serializers.SerializerMethodField()
    blog_posts = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()

    class Meta:
        model = Partner
        fields = [
            'id',
            'full_name',
            'email',
            'professional_title',
            'domain',
            'professional_summary',
            'website',
            'social_urls',
            'media_url',
            'avatar_url',
            'services',
            'affiliate_clients',
            'orders',
            'blog_posts',
            'projects',
            'created_at',
            'updated_at',
        ]

    def _build_absolute_url(self, path: str | None) -> str | None:
        if not path:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(path)
        return path

    def get_full_name(self, obj: Partner) -> str:
        # Use custom property 'full_name' defined on User instead of Django's default method
        name = getattr(obj.user, 'full_name', '')
        if name:
            return name
        # Fallback: derive from email local part
        return obj.user.email.split('@')[0].replace('.', ' ').title()

    def get_avatar_url(self, obj: Partner) -> str | None:
        if obj.media_url:
            return self._build_absolute_url(obj.media_url.url)
        if obj.user.profile_img:
            return self._build_absolute_url(obj.user.profile_img.url)
        return None

    def get_media_url(self, obj: Partner) -> str | None:
        if obj.media_url:
            return self._build_absolute_url(obj.media_url.url)
        return None

    def get_social_urls(self, obj: Partner) -> list[dict[str, str]]:
        raw = obj.social_urls or []
        cleaned: list[dict[str, str]] = []
        if isinstance(raw, dict):
            for key, url in raw.items():
                if url:
                    cleaned.append({'name': key, 'url': url})
        elif isinstance(raw, list):
            for entry in raw:
                if isinstance(entry, dict):
                    name = entry.get('name')
                    url = entry.get('url')
                    if name and url:
                        cleaned.append({'name': name, 'url': url})
        return cleaned

    def _ensure_list(self, value):
        if isinstance(value, list):
            return value
        if value is None:
            return []
        return list(value)

    def get_services(self, obj: Partner) -> list:
        return self._ensure_list(obj.services)

    def get_affiliate_clients(self, obj: Partner) -> list:
        return self._ensure_list(obj.affiliate_clients)

    def get_orders(self, obj: Partner) -> list:
        return self._ensure_list(obj.orders)

    def get_blog_posts(self, obj: Partner) -> list:
        return self._ensure_list(obj.blog_posts)

    def get_projects(self, obj: Partner) -> list:
        return self._ensure_list(obj.projects)


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Detailed user information for profile management
    """
    full_name = serializers.ReadOnlyField()
    can_change_password = serializers.ReadOnlyField()
    
    profile_img = serializers.ImageField(required=False, allow_null=True)
    partner_profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'role', 'is_active', 'date_joined', 'date_updated', 'profile_img', 'is_verified',
            'account_balance', 'currency', 'language_preference', 'user_timezone', 'affiliate_code', 'partner_profile',
            'two_factor_enabled', 'is_social_login', 'can_change_password'
        ]
        read_only_fields = ['id', 'date_joined', 'date_updated', 'role', 'email', 'is_verified', 'is_social_login', 'can_change_password']

    def get_partner_profile(self, obj):
        if hasattr(obj, 'partner_profile'):
            return PartnerSerializer(obj.partner_profile).data
        return None


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    User registration serializer with password validation
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name', 'phone', 
            'password', 'password_confirm'
        ]
    
    def validate(self, attrs):
        """Validate password confirmation"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs
    
    def validate_email(self, value):
        """Check if email already exists"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists.")
        return value
    
    def create(self, validated_data):
        """Create user with hashed password"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    User profile update serializer
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'currency', 'language_preference', 'user_timezone', 'affiliate_code']
    
    def validate_phone(self, value):
        """Validate phone number format"""
        if value and not value.startswith('+'):
            # Auto-format Kenyan numbers
            if value.startswith('0'):
                value = '+254' + value[1:]
            elif len(value) == 9:
                value = '+254' + value
        return value


class ClientProfileSerializer(serializers.ModelSerializer):
    """
    Client profile serializer with user information
    """
    user = UserBasicSerializer(read_only=True)
    
    class Meta:
        model = ClientProfile
        fields = [
            'user', 'company_name', 'industry', 'account_balance',
            'date_created', 'date_updated'
        ]
        read_only_fields = ['account_balance', 'date_created', 'date_updated']


class ClientProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Client profile update serializer
    """
    class Meta:
        model = ClientProfile
        fields = ['company_name', 'industry']


class PasswordChangeSerializer(serializers.Serializer):
    """
    Password change serializer for authenticated users
    """
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate_current_password(self, value):
        """Validate current password"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value
    
    def validate(self, attrs):
        """Validate new password confirmation"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match.")
        return attrs


class PasswordResetSerializer(serializers.Serializer):
    """
    Password reset request serializer
    """
    email = serializers.EmailField(required=True)
    
    def validate_email(self, value):
        """Normalize email"""
        return value.lower().strip()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Password reset confirmation serializer
    """
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True, min_length=6, max_length=6)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    
    def validate_code(self, value):
        """Validate verification code format"""
        if not value.isdigit():
            raise serializers.ValidationError("Code must be 6 digits.")
        return value
    
    def validate(self, attrs):
        """Normalize email"""
        attrs['email'] = attrs['email'].lower().strip()
        return attrs


class EmailVerificationSerializer(serializers.Serializer):
    """
    Email verification request serializer
    """
    email = serializers.EmailField(required=True)
    
    def validate_email(self, value):
        """Normalize email"""
        return value.lower().strip()


class EmailVerificationConfirmSerializer(serializers.Serializer):
    """
    Email verification confirmation serializer
    """
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True, min_length=6, max_length=6)
    
    def validate_code(self, value):
        """Validate verification code format"""
        if not value.isdigit():
            raise serializers.ValidationError("Code must be 6 digits.")
        return value
    
    def validate_email(self, value):
        """Normalize email"""
        return value.lower().strip()


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing user password."""
    
    current_password = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        help_text="Current password for verification"
    )
    new_password = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        help_text="New password"
    )
    confirm_password = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        help_text="Confirm new password"
    )

    def validate_current_password(self, value):
        """Validate that the current password is correct."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    def validate_new_password(self, value):
        """Validate the new password using Django's validators."""
        try:
            validate_password(value, self.context['request'].user)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def validate(self, attrs):
        """Validate that new password and confirm password match."""
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': "New password and confirmation password do not match."
            })
        
        # Check that new password is different from current password
        if attrs['current_password'] == attrs['new_password']:
            raise serializers.ValidationError({
                'new_password': "New password must be different from current password."
            })
        
        return attrs

    def save(self, **kwargs):
        """Change the user's password."""
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save(update_fields=['password'])
        return user


class Toggle2FASerializer(serializers.Serializer):
    """Serializer for toggling 2FA setting."""
    
    enabled = serializers.BooleanField(
        required=True,
        help_text="Enable or disable two-factor authentication"
    )

    def save(self, **kwargs):
        """Update the user's 2FA setting."""
        user = self.context['request'].user
        user.two_factor_enabled = self.validated_data['enabled']
        user.save(update_fields=['two_factor_enabled'])
        return user

