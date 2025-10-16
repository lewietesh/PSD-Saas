# core/serializers.py
from rest_framework import serializers
from .models import (
    ContactInfo, NewsletterSubscription, HeroSection, AboutSection,
    WorkExperience, AboutStats, WhyChooseUs, Roadmap,
    SupportTicket, SupportAttachment
)
from accounts.serializers import UserBasicSerializer

# Newsletter Subscription Serializer
class NewsletterSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscription
        fields = ['id', 'email', 'date_subscribed']
        read_only_fields = ['id', 'date_subscribed']

# ContactInfo serializer
class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = [
            'id', 'brand_name', 'email', 'phone', 'location', 'social_links', 'date_created', 'date_updated'
        ]
        read_only_fields = ['id', 'date_created', 'date_updated']

# Work Experience Serializers
class WorkExperienceSerializer(serializers.ModelSerializer):
    duration_text = serializers.ReadOnlyField()
    duration_months = serializers.ReadOnlyField()
    
    class Meta:
        model = WorkExperience
        fields = [
            'id', 'company_name', 'job_title', 'industry', 'company_logo', 'company_website',
            'start_month', 'start_year', 'end_month', 'end_year', 'is_current',
            'description', 'key_responsibilities', 'achievements', 'technology_stack',
            'is_featured', 'display_order', 'duration_text', 'duration_months',
            'date_created', 'date_updated'
        ]
        read_only_fields = ['id', 'duration_text', 'duration_months', 'date_created', 'date_updated']

class PublicWorkExperienceSerializer(serializers.ModelSerializer):
    """Public serializer for work experience - only featured experiences"""
    duration_text = serializers.ReadOnlyField()
    duration_months = serializers.ReadOnlyField()
    
    class Meta:
        model = WorkExperience
        fields = [
            'id', 'company_name', 'job_title', 'industry', 'company_logo', 'company_website',
            'description', 'key_responsibilities', 'achievements', 'technology_stack',
            'duration_text', 'duration_months'
        ]

# About Stats Serializers
class AboutStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutStats
        fields = [
            'id', 'stat_name', 'stat_value', 'stat_description', 'icon_name',
            'display_order', 'is_active', 'date_created', 'date_updated'
        ]
        read_only_fields = ['id', 'date_created', 'date_updated']

class PublicAboutStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutStats
        fields = ['stat_name', 'stat_value', 'stat_description', 'icon_name']

# Why Choose Us Serializers
class WhyChooseUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhyChooseUs
        fields = [
            'id', 'reason_title', 'reason_description', 'icon_name',
            'display_order', 'is_active', 'date_created', 'date_updated'
        ]
        read_only_fields = ['id', 'date_created', 'date_updated']

class PublicWhyChooseUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhyChooseUs
        fields = ['reason_title', 'reason_description', 'icon_name']

# Roadmap Serializers
class RoadmapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roadmap
        fields = [
            'id', 'milestone_title', 'milestone_description', 'target_date',
            'is_completed', 'completion_date', 'icon_name', 'display_order',
            'is_active', 'date_created', 'date_updated'
        ]
        read_only_fields = ['id', 'date_created', 'date_updated']

class PublicRoadmapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roadmap
        fields = [
            'milestone_title', 'milestone_description', 'target_date',
            'is_completed', 'completion_date', 'icon_name'
        ]

# Hero Section Serializers
class HeroSectionSerializer(serializers.ModelSerializer):
    """
    Serializer for HeroSection model
    Used for homepage hero content management
    """
    
    class Meta:
        model = HeroSection
        fields = [
            'id',
            'page',
            'heading',
            'subheading',
            'cta_text',
            'cta_link',
            'is_active',
            'date_created',
            'date_updated'
        ]
        read_only_fields = ['id', 'date_created', 'date_updated']
    
    def validate_heading(self, value):
        """Ensure heading is not empty"""
        if not value.strip():
            raise serializers.ValidationError("Heading cannot be empty.")
        return value.strip()
    
    def validate_cta_link(self, value):
        """Validate CTA link format if provided"""
        if value and not (value.startswith('http://') or value.startswith('https://') or value.startswith('/')):
            raise serializers.ValidationError("CTA link must be a valid URL or relative path.")
        return value

class HeroSectionListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for hero section lists
    """
    
    class Meta:
        model = HeroSection
        fields = ['id', 'heading', 'is_active', 'date_created']

class PublicHeroSectionSerializer(serializers.ModelSerializer):
    """
    Public serializer for active hero section
    Only returns essential fields for frontend
    """
    
    class Meta:
        model = HeroSection
        fields = ['page', 'heading', 'subheading', 'cta_text', 'cta_link']

# About Section Serializers
class AboutSectionSerializer(serializers.ModelSerializer):
    """
    Serializer for AboutSection model
    Used for about page content management
    """
    
    social_links_count = serializers.SerializerMethodField()
    
    class Meta:
        model = AboutSection
        fields = [
            'id',
            'title',
            'description', 
            'media',
            'socials_urls',
            'show_stats',
            'show_work_experience',
            'show_why_choose_us',
            'show_roadmap',
            'social_links_count',
            'date_created',
            'date_updated'
        ]
        read_only_fields = ['id', 'date_created', 'date_updated', 'social_links_count']
    
    def get_social_links_count(self, obj):
        """Return count of social media links"""
        if obj.socials_urls:
            return len(obj.socials_urls)
        return 0
    
    def validate_title(self, value):
        """Ensure title is not empty"""
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value.strip()
    
    def validate_description(self, value):
        """Ensure description is not empty and has minimum length"""
        if not value.strip():
            raise serializers.ValidationError("Description cannot be empty.")
        if len(value.strip()) < 50:
            raise serializers.ValidationError("Description must be at least 50 characters long.")
        return value.strip()
    
    def validate_media_url(self, value):
        """Validate media URL format if provided"""
        if value and not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError("Media URL must be a valid HTTP/HTTPS URL.")
        return value
    
    def validate_socials_urls(self, value):
        """Validate social media URLs structure"""
        if not value:
            return value
        
        if not isinstance(value, list):
            raise serializers.ValidationError("Social URLs must be a list.")
        
        for social in value:
            if not isinstance(social, dict):
                raise serializers.ValidationError("Each social link must be an object with 'name' and 'url' fields.")
            
            if 'name' not in social or 'url' not in social:
                raise serializers.ValidationError("Each social link must have 'name' and 'url' fields.")
            
            if not social['name'].strip():
                raise serializers.ValidationError("Social media name cannot be empty.")
            
            if not social['url'].startswith(('http://', 'https://')):
                raise serializers.ValidationError(f"Social media URL for {social['name']} must be a valid HTTP/HTTPS URL.")
        
        return value

class AboutSectionListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for about section lists
    """
    
    class Meta:
        model = AboutSection
        fields = ['id', 'title','description', 
            'media',
            'socials_urls', 'date_created']

class PublicAboutSectionSerializer(serializers.ModelSerializer):
    """
    Public serializer for about section
    Only returns essential fields for frontend
    """
    
    class Meta:
        model = AboutSection
        fields = ['title', 'description', 'media', 'socials_urls']

# Complete About Page Data Serializer
class CompleteAboutDataSerializer(serializers.Serializer):
    """
    Serializer that combines all about page data for frontend consumption
    """
    about_section = PublicAboutSectionSerializer()
    work_experience = PublicWorkExperienceSerializer(many=True)
    stats = PublicAboutStatsSerializer(many=True)


# Support Ticket Serializers
class SupportAttachmentSerializer(serializers.ModelSerializer):
    """Serializer for support ticket attachments."""
    
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = SupportAttachment
        fields = [
            'id', 'file', 'file_url', 'original_filename', 
            'file_size', 'file_extension', 'is_image', 'uploaded_at'
        ]
        read_only_fields = ['id', 'original_filename', 'file_size', 'uploaded_at']
    
    def get_file_url(self, obj):
        """Get absolute URL for the attachment file."""
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None


class SupportTicketSerializer(serializers.ModelSerializer):
    """Full serializer for support tickets with all details."""
    
    user = UserBasicSerializer(read_only=True)
    admin_user = UserBasicSerializer(read_only=True) 
    attachments = SupportAttachmentSerializer(many=True, read_only=True)
    messages_count = serializers.ReadOnlyField()
    
    class Meta:
        model = SupportTicket
        fields = [
            'id', 'user', 'subject', 'message', 'priority', 'status',
            'admin_reply', 'admin_user', 'attachments', 'messages_count',
            'created_at', 'updated_at', 'resolved_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'resolved_at']


class SupportTicketCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating support tickets."""
    
    class Meta:
        model = SupportTicket
        fields = ['subject', 'message', 'priority']
    
    def validate_subject(self, value):
        """Validate subject length."""
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Subject must be at least 5 characters long.")
        return value.strip()
    
    def validate_message(self, value):
        """Validate message length."""
        if len(value.strip()) < 20:
            raise serializers.ValidationError("Message must be at least 20 characters long.")
        return value.strip()


class SupportTicketListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for support ticket lists."""
    
    messages_count = serializers.ReadOnlyField()
    attachment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = SupportTicket
        fields = [
            'id', 'subject', 'priority', 'status', 'messages_count',
            'attachment_count', 'created_at', 'updated_at'
        ]
    
    def get_attachment_count(self, obj):
        """Get count of attachments."""
        return obj.attachments.count()