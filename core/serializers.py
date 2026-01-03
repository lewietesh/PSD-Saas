# core/serializers.py
from rest_framework import serializers
from .models import (
    ContactInfo, NewsletterSubscription, HeroSection, AboutSection,
    WorkExperience, AboutStats, WhyChooseUs, Roadmap,
    SupportTicket, SupportAttachment, FAQ
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
            'start_month', 'start_year', 'end_month', 'end_year', 'is_current',
            'description', 'key_responsibilities', 'achievements', 'technology_stack',
            'duration_text', 'duration_months'
        ]

# About Stats Serializers
class AboutStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutStats
        fields = [
            'id', 'label', 'value', 'icon', 'display_order', 'is_active',
            'date_created', 'date_updated'
        ]
        read_only_fields = ['id', 'date_created', 'date_updated']

class PublicAboutStatsSerializer(serializers.ModelSerializer):
    """Public serializer for about stats - only active stats"""
    class Meta:
        model = AboutStats
        fields = ['id', 'label', 'value', 'icon', 'display_order']

# WhyChooseUs Serializers
class WhyChooseUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhyChooseUs
        fields = [
            'id', 'reason_title', 'reason_description', 'img', 'display_order', 'is_active',
            'date_created', 'date_updated'
        ]
        read_only_fields = ['id', 'date_created', 'date_updated']

class PublicWhyChooseUsSerializer(serializers.ModelSerializer):
    """Public serializer for why choose us - only active items"""
    class Meta:
        model = WhyChooseUs
        fields = ['id', 'reason_title', 'reason_description', 'img', 'display_order']

# Roadmap Serializers
class RoadmapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roadmap
        fields = [
            'id', 'milestone_title', 'milestone_description', 'target_date', 
            'is_completed', 'completion_date', 'icon_name',
            'display_order', 'is_active', 'date_created', 'date_updated'
        ]
        read_only_fields = ['id', 'date_created', 'date_updated']

class PublicRoadmapSerializer(serializers.ModelSerializer):
    """Public serializer for roadmap - only active items"""
    class Meta:
        model = Roadmap
        fields = [
            'id', 'milestone_title', 'milestone_description', 'target_date', 
            'is_completed', 'completion_date', 'icon_name', 'display_order'
        ]

# Hero Section Serializers
class HeroSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroSection
        fields = [
            'id', 'page', 'headline', 'subheadline', 'cta_text', 'cta_link', 'cta_secondary_text', 
            'cta_secondary_link', 'background_video', 'background_image', 'is_active', 
            'date_created', 'date_updated'
        ]
        read_only_fields = ['id', 'date_created', 'date_updated']

class HeroSectionListSerializer(serializers.ModelSerializer):
    """Lightweight list serializer"""
    class Meta:
        model = HeroSection
        fields = ['id', 'page', 'headline', 'is_active', 'date_created']
        read_only_fields = fields

class PublicHeroSectionSerializer(serializers.ModelSerializer):
    """Public serializer for hero sections - only active hero"""
    class Meta:
        model = HeroSection
        fields = [
            'id', 'page', 'headline', 'subheadline', 'cta_text', 'cta_link',
            'cta_secondary_text', 'cta_secondary_link', 'background_video', 'background_image'
        ]

# About Section Serializers
class AboutSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutSection
        fields = [
            'id', 'title', 'description', 'profile_img', 'profile_video', 'quote', 
            'is_active', 'date_created', 'date_updated'
        ]
        read_only_fields = ['id', 'date_created', 'date_updated']

class AboutSectionListSerializer(serializers.ModelSerializer):
    """Lightweight list serializer"""
    class Meta:
        model = AboutSection
        fields = ['id', 'title', 'is_active', 'date_created']
        read_only_fields = fields

class PublicAboutSectionSerializer(serializers.ModelSerializer):
    """Public serializer for about sections - only active about"""
    class Meta:
        model = AboutSection
        fields = ['id', 'title', 'description', 'profile_img', 'profile_video', 'quote']

# Complete About Data Serializer
class CompleteAboutDataSerializer(serializers.Serializer):
    """
    Serializer that combines all about-related data in one response.
    Used for the public about page to reduce API calls.
    """
    about_section = PublicAboutSectionSerializer()
    work_experience = PublicWorkExperienceSerializer(many=True)
    stats = PublicAboutStatsSerializer(many=True)
    why_choose_us = PublicWhyChooseUsSerializer(many=True)
    roadmap = PublicRoadmapSerializer(many=True)

# Support Ticket Serializers
class SupportAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportAttachment
        fields = ['id', 'file', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']

class SupportTicketSerializer(serializers.ModelSerializer):
    """Serializer for viewing support tickets"""
    user_details = UserBasicSerializer(source='user', read_only=True)
    attachments = SupportAttachmentSerializer(many=True, read_only=True)
    attachment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = SupportTicket
        fields = [
            'id', 'user', 'user_details', 'subject', 'message', 'status',
            'priority', 'admin_reply', 'admin_user', 'attachments', 'attachment_count',
            'created_at', 'updated_at', 'resolved_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'resolved_at', 'admin_user']
    
    def get_attachment_count(self, obj):
        """Get count of attachments."""
        return obj.attachments.count()


class SupportTicketCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating support tickets"""
    attachment_files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = SupportTicket
        fields = [
            'subject', 'message', 'priority', 'attachment_files'
        ]
    
    def create(self, validated_data):
        attachment_files = validated_data.pop('attachment_files', [])
        ticket = SupportTicket.objects.create(**validated_data)
        
        # Create attachments
        for file in attachment_files:
            SupportAttachment.objects.create(ticket=ticket, file=file)
        
        return ticket

class SupportTicketListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing tickets"""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    attachment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = SupportTicket
        fields = [
            'id', 'user_email', 'subject', 'message', 'status', 'priority',
            'attachment_count', 'created_at', 'updated_at', 'resolved_at'
        ]
        read_only_fields = fields

    def get_attachment_count(self, obj):
        return obj.attachments.count()

# FAQ Serializers
class FAQSerializer(serializers.ModelSerializer):
    """Serializer for FAQ model - both admin and public use"""
    
    class Meta:
        model = FAQ
        fields = [
            'id', 'question', 'answer', 'featured', 'links',
            'display_order', 'is_active', 'date_created', 'date_updated'
        ]
        read_only_fields = ['id', 'date_created', 'date_updated']

class PublicFAQSerializer(serializers.ModelSerializer):
    """Public serializer for FAQs - only active FAQs"""
    
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'featured', 'links']
        read_only_fields = ['id']
