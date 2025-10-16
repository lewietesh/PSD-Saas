# core/admin.py
from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    HeroSection, AboutSection, ContactInfo, NewsletterSubscription,
    WorkExperience, AboutStats, WhyChooseUs, Roadmap,
    SupportTicket, SupportAttachment
)

# NewsletterSubscription admin
@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_subscribed')
    search_fields = ('email',)
    list_filter = ('date_subscribed',)
    ordering = ('-date_subscribed',)
    readonly_fields = ('email', 'date_subscribed')

# Custom form for ContactInfo to enhance social_links input
class ContactInfoAdminForm(forms.ModelForm):
    social_links_ig = forms.URLField(label='Instagram', required=False)
    social_links_git = forms.URLField(label='GitHub', required=False)
    social_links_linkedin = forms.URLField(label='LinkedIn', required=False)
    social_links_x = forms.URLField(label='X (Twitter)', required=False)
    social_links_reddit = forms.URLField(label='Reddit', required=False)

    class Meta:
        model = ContactInfo
        fields = ['brand_name', 'email', 'phone', 'location',
                  'social_links_ig', 'social_links_git', 'social_links_linkedin', 'social_links_x', 'social_links_reddit']
        widgets = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate initial values from social_links JSON
        social = self.instance.social_links or {}
        self.fields['social_links_ig'].initial = social.get('ig', '')
        self.fields['social_links_git'].initial = social.get('git', '')
        self.fields['social_links_linkedin'].initial = social.get('linkedin', '')
        self.fields['social_links_x'].initial = social.get('x', '')
        self.fields['social_links_reddit'].initial = social.get('reddit', '')

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['social_links'] = {
            'ig': cleaned_data.get('social_links_ig', ''),
            'git': cleaned_data.get('social_links_git', ''),
            'linkedin': cleaned_data.get('social_links_linkedin', ''),
            'x': cleaned_data.get('social_links_x', ''),
            'reddit': cleaned_data.get('social_links_reddit', ''),
        }
        return cleaned_data

    def save(self, commit=True):
        self.instance.social_links = self.cleaned_data['social_links']
        return super().save(commit=commit)

# Admin for ContactInfo with social links preview and enhanced form
@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    form = ContactInfoAdminForm
    list_display = ('brand_name', 'email', 'phone', 'location', 'social_links_preview', 'date_created', 'date_updated')
    search_fields = ('brand_name', 'email', 'phone', 'location')
    readonly_fields = ('date_created', 'date_updated', 'social_links_preview')
    ordering = ('-date_created',)

    def get_fields(self, request, obj=None):
        fields = ['brand_name', 'email', 'phone', 'location',
                  'social_links_ig', 'social_links_git', 'social_links_linkedin', 'social_links_x', 'social_links_reddit',
                  'social_links_preview', 'date_created', 'date_updated']
        return fields

    def social_links_preview(self, obj):
        if obj.social_links:
            links = []
            for key, url in obj.social_links.items():
                if url:
                    links.append(f"<a href='{url}' target='_blank'>{key}</a>")
            return mark_safe(', '.join(links))
        return "-"
    social_links_preview.short_description = "Social Links"

# Work Experience Admin
@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = [
        'company_name', 'job_title', 'duration_display', 'industry',
        'is_current', 'is_featured', 'display_order'
    ]
    list_filter = ['is_current', 'is_featured', 'industry', 'start_year']
    search_fields = ['company_name', 'job_title', 'industry']
    readonly_fields = ['date_created', 'date_updated', 'duration_text', 'duration_months']
    
    fieldsets = (
        ('Company Information', {
            'fields': ('company_name', 'job_title', 'industry', 'company_logo', 'company_website')
        }),
        ('Duration', {
            'fields': ('start_month', 'start_year', 'end_month', 'end_year', 'is_current', 'duration_text', 'duration_months'),
        }),
        ('Job Details', {
            'fields': ('description', 'key_responsibilities', 'achievements', 'technology_stack')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'display_order')
        }),
        ('Timestamps', {
            'fields': ('date_created', 'date_updated'),
            'classes': ('collapse',)
        }),
    )
    
    def duration_display(self, obj):
        return obj.duration_text
    duration_display.short_description = 'Duration'
    
    actions = ['mark_as_featured', 'mark_as_not_featured']
    
    def mark_as_featured(self, request, queryset):
        count = queryset.update(is_featured=True)
        self.message_user(request, f'{count} experiences marked as featured.')
    mark_as_featured.short_description = "Mark selected as featured"
    
    def mark_as_not_featured(self, request, queryset):
        count = queryset.update(is_featured=False)
        self.message_user(request, f'{count} experiences marked as not featured.')
    mark_as_not_featured.short_description = "Mark selected as not featured"

# About Stats Admin
@admin.register(AboutStats)
class AboutStatsAdmin(admin.ModelAdmin):
    list_display = ['stat_name', 'stat_value', 'stat_description_preview', 'icon_name', 'is_active', 'display_order']
    list_filter = ['is_active', 'date_created']
    search_fields = ['stat_name', 'stat_value', 'stat_description']
    readonly_fields = ['date_created', 'date_updated']
    ordering = ['display_order', 'stat_name']
    
    def stat_description_preview(self, obj):
        if obj.stat_description:
            return (obj.stat_description[:50] + '...') if len(obj.stat_description) > 50 else obj.stat_description
        return '-'
    stat_description_preview.short_description = 'Description'
    
    actions = ['activate_stats', 'deactivate_stats']
    
    def activate_stats(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} stats activated.')
    activate_stats.short_description = "Activate selected stats"
    
    def deactivate_stats(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} stats deactivated.')
    deactivate_stats.short_description = "Deactivate selected stats"

# Why Choose Us Admin
@admin.register(WhyChooseUs)
class WhyChooseUsAdmin(admin.ModelAdmin):
    list_display = ['reason_title', 'reason_description_preview', 'icon_name', 'is_active', 'display_order']
    list_filter = ['is_active', 'date_created']
    search_fields = ['reason_title', 'reason_description']
    readonly_fields = ['date_created', 'date_updated']
    ordering = ['display_order', 'reason_title']
    
    def reason_description_preview(self, obj):
        if obj.reason_description:
            return (obj.reason_description[:75] + '...') if len(obj.reason_description) > 75 else obj.reason_description
        return '-'
    reason_description_preview.short_description = 'Description'
    
    actions = ['activate_reasons', 'deactivate_reasons']
    
    def activate_reasons(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} reasons activated.')
    activate_reasons.short_description = "Activate selected reasons"
    
    def deactivate_reasons(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} reasons deactivated.')
    deactivate_reasons.short_description = "Deactivate selected reasons"

# Roadmap Admin
@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    list_display = [
        'milestone_title', 'milestone_description_preview', 'target_date', 
        'is_completed', 'completion_date', 'is_active', 'display_order'
    ]
    list_filter = ['is_completed', 'is_active', 'target_date', 'date_created']
    search_fields = ['milestone_title', 'milestone_description']
    readonly_fields = ['date_created', 'date_updated']
    ordering = ['display_order', 'target_date']
    
    def milestone_description_preview(self, obj):
        if obj.milestone_description:
            return (obj.milestone_description[:75] + '...') if len(obj.milestone_description) > 75 else obj.milestone_description
        return '-'
    milestone_description_preview.short_description = 'Description'
    
    actions = ['mark_completed', 'mark_not_completed', 'activate_milestones', 'deactivate_milestones']
    
    def mark_completed(self, request, queryset):
        from django.utils import timezone
        count = queryset.update(is_completed=True, completion_date=timezone.now().date())
        self.message_user(request, f'{count} milestones marked as completed.')
    mark_completed.short_description = "Mark selected as completed"
    
    def mark_not_completed(self, request, queryset):
        count = queryset.update(is_completed=False, completion_date=None)
        self.message_user(request, f'{count} milestones marked as not completed.')
    mark_not_completed.short_description = "Mark selected as not completed"
    
    def activate_milestones(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} milestones activated.')
    activate_milestones.short_description = "Activate selected milestones"
    
    def deactivate_milestones(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} milestones deactivated.')
    deactivate_milestones.short_description = "Deactivate selected milestones"

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    """
    Admin interface for HeroSection model
    """
    
    list_display = [
        'heading', 
        'subheading_preview', 
        'page',
        'is_active_display', 
        'has_cta',
        'date_created',
        'date_updated'
    ]
    list_filter = ['is_active', 'page', 'date_created']
    search_fields = ['heading', 'subheading']
    readonly_fields = ['date_created', 'date_updated']
    
    fieldsets = (
        ('Content', {
            'fields': ('page', 'heading', 'subheading')
        }),
        ('Call to Action', {
            'fields': ('cta_text', 'cta_link'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('date_created', 'date_updated'),
            'classes': ('collapse',)
        }),
    )
    
    def subheading_preview(self, obj):
        """Show truncated subheading in list view"""
        if obj.subheading:
            return (obj.subheading[:50] + '...') if len(obj.subheading) > 50 else obj.subheading
        return '-'
    subheading_preview.short_description = 'Subheading Preview'
    
    def is_active_display(self, obj):
        """Display active status with color coding"""
        if obj.is_active:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Active</span>'
            )
        return format_html(
            '<span style="color: red;">✗ Inactive</span>'
        )
    is_active_display.short_description = 'Status'
    
    def has_cta(self, obj):
        """Check if hero section has call-to-action"""
        return bool(obj.cta_text and obj.cta_link)
    has_cta.boolean = True
    has_cta.short_description = 'Has CTA'
    
    actions = ['activate_hero', 'deactivate_hero']
    
    def activate_hero(self, request, queryset):
        """Custom action to activate selected hero (deactivates others)"""
        if queryset.count() > 1:
            self.message_user(
                request, 
                "You can only activate one hero section at a time.", 
                level='error'
            )
            return
        
        # Deactivate all others for the same page
        hero = queryset.first()
        HeroSection.objects.filter(page=hero.page).update(is_active=False)
        # Activate selected
        queryset.update(is_active=True)
        
        self.message_user(
            request, 
            f"Successfully activated hero section: {hero.heading}"
        )
    activate_hero.short_description = "Activate selected hero section"
    
    def deactivate_hero(self, request, queryset):
        """Custom action to deactivate selected heroes"""
        count = queryset.update(is_active=False)
        self.message_user(
            request, 
            f"Successfully deactivated {count} hero section(s)."
        )
    deactivate_hero.short_description = "Deactivate selected hero sections"
    
    def save_model(self, request, obj, form, change):
        """Override save to handle business logic"""
        # If setting this as active, deactivate others for the same page
        if obj.is_active:
            HeroSection.objects.filter(page=obj.page).exclude(pk=obj.pk).update(is_active=False)
        super().save_model(request, obj, form, change)

@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    """
    Admin interface for AboutSection model
    """
    
    list_display = [
        'title', 
        'description_preview',
        'media',
        'social_links_count',
        'show_work_experience',
        'show_stats',
        'show_why_choose_us',
        'show_roadmap',
        'date_created',
        'date_updated'
    ]
    list_filter = ['show_work_experience', 'show_stats', 'show_why_choose_us', 'show_roadmap', 'date_created']
    search_fields = ['title', 'description']
    readonly_fields = ['date_created', 'date_updated', 'preview_socials']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description')
        }),
        ('Media', {
            'fields': ('media',),
            'classes': ('collapse',)
        }),
        ('Display Options', {
            'fields': ('show_stats', 'show_work_experience', 'show_why_choose_us', 'show_roadmap')
        }),
        ('Social Media Links', {
            'fields': ('socials_urls', 'preview_socials'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('date_created', 'date_updated'),
            'classes': ('collapse',)
        }),
    )
    
    def description_preview(self, obj):
        """Show truncated description in list view"""
        if obj.description:
            return (obj.description[:75] + '...') if len(obj.description) > 75 else obj.description
        return '-'
    description_preview.short_description = 'Description Preview'
    
    def social_links_count(self, obj):
        """Count of social media links"""
        if obj.socials_urls:
            return len(obj.socials_urls)
        return 0
    social_links_count.short_description = 'Social Links'
    
    def preview_socials(self, obj):
        """Preview social media links in admin"""
        if not obj.socials_urls:
            return "No social links configured"
        
        links_html = []
        for social in obj.socials_urls:
            name = social.get('name', 'Unknown')
            url = social.get('url', '#')
            links_html.append(
                f'<a href="{url}" target="_blank" style="margin-right: 10px; '
                f'display: inline-block; padding: 2px 6px; background: #f0f0f0; '
                f'border-radius: 3px; text-decoration: none; color: #333;">{name}</a>'
            )
        
        return mark_safe(''.join(links_html))
    preview_socials.short_description = 'Social Media Preview'
    
    def get_queryset(self, request):
        """Optimize queryset for admin list view"""
        return super().get_queryset(request).order_by('-date_created')

# Support Ticket Admin
class SupportAttachmentInline(admin.TabularInline):
    model = SupportAttachment
    extra = 0
    readonly_fields = ('original_filename', 'file_size', 'uploaded_at')
    fields = ('file', 'original_filename', 'file_size', 'uploaded_at')


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'user', 'priority', 'status', 'created_at', 'has_reply')
    list_filter = ('status', 'priority', 'created_at')
    search_fields = ('subject', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at', 'resolved_at', 'messages_count')
    inlines = [SupportAttachmentInline]
    
    fieldsets = (
        ('Ticket Information', {
            'fields': ('user', 'subject', 'message', 'priority', 'status')
        }),
        ('Admin Response', {
            'fields': ('admin_reply', 'admin_user'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'resolved_at', 'messages_count'),
            'classes': ('collapse',)
        }),
    )
    
    def has_reply(self, obj):
        """Check if ticket has admin reply."""
        return bool(obj.admin_reply)
    has_reply.boolean = True
    has_reply.short_description = 'Has Reply'
    
    def save_model(self, request, obj, form, change):
        """Set admin_user when admin_reply is added."""
        if obj.admin_reply and not obj.admin_user:
            obj.admin_user = request.user
        super().save_model(request, obj, form, change)


@admin.register(SupportAttachment)
class SupportAttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticket', 'original_filename', 'file_size', 'uploaded_at', 'is_image')
    list_filter = ('uploaded_at',)
    search_fields = ('ticket__subject', 'original_filename')
    readonly_fields = ('original_filename', 'file_size', 'uploaded_at')

# Admin site customization
# admin.site.site_header = "Portfolio API Administration"
# admin.site.site_title = "Portfolio Admin"
# admin.site.index_title = "Welcome to Portfolio Administration"