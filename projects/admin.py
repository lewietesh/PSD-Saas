# projects/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Count
from django.db import models
from django import forms
from django.utils import timezone
import json
from .models import (
    Technology, Project, ProjectGalleryImage, ProjectSection,
    ProjectComment, ProjectTechnology
)
from accounts.admin import BaseAdminPermissions


@admin.register(Technology)
class TechnologyAdmin(BaseAdminPermissions):
    """
    Admin interface for Technology model
    """
    
    list_display = ['name', 'category', 'icon_display', 'projects_count', 'id']
    list_filter = ['category']
    search_fields = ['name', 'category']
    readonly_fields = ['projects_count']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category')
        }),
        ('Display', {
            'fields': ('icon_url',),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('projects_count',),
            'classes': ('collapse',)
        }),
    )
    
    def icon_display(self, obj):
        """Display technology icon if available"""
        if obj.icon_url:
            return format_html(
                '<img src="{}" style="width: 24px; height: 24px;" alt="{}" />',
                obj.icon_url, obj.name
            )
        return '-'
    icon_display.short_description = 'Icon'
    
    def projects_count(self, obj):
        """Count of completed projects using this technology"""
        return obj.projects.filter(status='completed').count()
    projects_count.short_description = 'Completed Projects'
    
    def get_queryset(self, request):
        """Optimize queryset with project counts"""
        return super().get_queryset(request).annotate(
            projects_count=Count('projects')
        )


class ProjectSectionInline(admin.StackedInline):
    """
    Inline admin for project sections - USER FRIENDLY!
    Upload images directly, no URLs needed!
    """
    model = ProjectSection
    extra = 1
    fields = ['section_id', 'section_name', 'media', 'image_preview', 'description', 'sort_order', 'is_active']
    readonly_fields = ['image_preview']
    ordering = ['sort_order']
    
    def image_preview(self, obj):
        """Display section image preview in admin"""
        if obj.media:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.media.url
            )
        return mark_safe('<span style="color: #999;">No image uploaded yet</span>')
    image_preview.short_description = 'Image Preview'
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        # Add helpful placeholder text
        formset.form.base_fields['section_name'].widget.attrs['placeholder'] = 'Optional: Custom section name (defaults to section type)'
        formset.form.base_fields['description'].widget.attrs['rows'] = 4
        formset.form.base_fields['description'].widget.attrs['placeholder'] = 'Detailed description for this section...'
        return formset


class ProjectGalleryImageInline(admin.TabularInline):
    """
    Inline admin for project gallery images
    """
    model = ProjectGalleryImage
    extra = 1
    fields = ['image', 'alt_text', 'sort_order', 'image_preview']
    readonly_fields = ['image_preview']
    ordering = ['sort_order']
    
    def image_preview(self, obj):
        """Display image preview in admin"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 60px;" />',
                obj.image.url
            )
        return '-'
    image_preview.short_description = 'Preview'


class ProjectTechnologyInline(admin.TabularInline):
    """
    Inline admin for project technologies
    """
    model = ProjectTechnology
    extra = 1
    autocomplete_fields = ['technology']


class ProjectCommentInline(admin.TabularInline):
    """
    Inline admin for project comments
    """
    model = ProjectComment
    extra = 0
    readonly_fields = ['name', 'email', 'message', 'date_created', 'approved']
    fields = ['name', 'email', 'message', 'approved', 'date_created']
    can_delete = True
    
    def has_add_permission(self, request, obj=None):
        """Disable adding comments through inline"""
        return False


@admin.register(Project)
class ProjectAdmin(BaseAdminPermissions):
    """
    Admin interface for Project model
    """
    
    list_display = [
        'title',
        'client',
        'author',
        'status_display',
        'featured_display',
        'category',
        'likes',
        'comments_count',
        'technologies_count',
        'completion_date',
        'date_created'
    ]
    list_filter = [
        'status',
        'featured',
        'category',
        'domain',
        'client',
        'author',
        'completion_date',
        'date_created',
        # Removed 'technologies' from list_filter since it has a through model
    ]
    search_fields = ['title', 'description', 'content', 'category', 'domain', 'author__email', 'author__first_name', 'author__last_name']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = [
        'id',
        'likes',
        'date_created',
        'date_updated',
        'comments_count',
        'technologies_count',
        'gallery_images_count',
        'sections_count',
        'image_preview'
    ]
    
    # Removed filter_horizontal for technologies since it has a through model
    inlines = [
        ProjectSectionInline,  # NEW: User-friendly section management!
        ProjectGalleryImageInline, 
        ProjectTechnologyInline,
        ProjectCommentInline
    ]
    autocomplete_fields = ['client', 'author']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'domain', 'client', 'author')
        }),
        ('Content', {
            'fields': ('description', 'content', 'image', 'image_preview')
        }),
        ('Project Links', {
            'fields': ('url', 'repository_url'),
            'classes': ('collapse',)
        }),
        ('Project Status', {
            'fields': ('status', 'completion_date', 'featured'),
            'classes': ('collapse',)
        }),
        # Removed 'Technologies' fieldset since technologies can't be in fieldsets with through model
        ('Statistics', {
            'fields': ('likes', 'comments_count', 'technologies_count', 'gallery_images_count', 'sections_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('id', 'date_created', 'date_updated'),
            'classes': ('collapse',)
        }),
    )
    
    def status_display(self, obj):
        """Display status with color coding"""
        colors = {
            'ongoing': '#ffc107',      # Yellow
            'completed': '#28a745',    # Green
            'maintenance': '#17a2b8'   # Blue
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="color: {}; font-weight: bold;">● {}</span>',
            color, obj.status.title()
        )
    status_display.short_description = 'Status'
    
    def featured_display(self, obj):
        """Display featured status"""
        if obj.featured:
            return format_html('<span style="color: gold;">⭐ Featured</span>')
        return '-'
    featured_display.short_description = 'Featured'
    
    def comments_count(self, obj):
        """Count of approved comments"""
        return obj.comments.filter(approved=True).count()
    comments_count.short_description = 'Comments'
    
    def technologies_count(self, obj):
        """Count of technologies used"""
        return obj.technologies.count()
    technologies_count.short_description = 'Technologies'
    
    def gallery_images_count(self, obj):
        """Count of gallery images"""
        return obj.gallery_images.count()
    gallery_images_count.short_description = 'Gallery Images'
    
    def sections_count(self, obj):
        """Count of project sections"""
        return obj.project_sections.filter(is_active=True).count()
    sections_count.short_description = 'Active Sections'
    
    def image_preview(self, obj):
        """Display featured image preview in admin"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 150px; border-radius: 8px;" />',
                obj.image.url
            )
        return '-'
    image_preview.short_description = 'Featured Image Preview'
    
    actions = ['complete_projects', 'feature_projects', 'unfeature_projects', 'mark_maintenance']
    
    def complete_projects(self, request, queryset):
        """Mark selected projects as completed"""
        updated = queryset.update(
            status='completed',
            completion_date=timezone.now().date()
        )
        self.message_user(request, f"Successfully completed {updated} project(s).")
    complete_projects.short_description = "Mark selected projects as completed"
    
    def feature_projects(self, request, queryset):
        """Feature selected projects"""
        updated = queryset.update(featured=True)
        self.message_user(request, f"Successfully featured {updated} project(s).")
    feature_projects.short_description = "Feature selected projects"
    
    def unfeature_projects(self, request, queryset):
        """Unfeature selected projects"""
        updated = queryset.update(featured=False)
        self.message_user(request, f"Successfully unfeatured {updated} project(s).")
    unfeature_projects.short_description = "Unfeature selected projects"
    
    def mark_maintenance(self, request, queryset):
        """Mark selected projects as in maintenance"""
        updated = queryset.update(status='maintenance')
        self.message_user(request, f"Successfully marked {updated} project(s) as in maintenance.")
    mark_maintenance.short_description = "Mark selected projects as maintenance"
    
    def get_queryset(self, request):
        """Optimize queryset with related data"""
        return super().get_queryset(request).select_related(
            'client', 'author'
        ).prefetch_related('technologies', 'gallery_images', 'comments')


@admin.register(ProjectComment)
class ProjectCommentAdmin(BaseAdminPermissions):
    """
    Admin interface for ProjectComment model
    """
    
    list_display = [
        'name',
        'email',
        'project_title',
        'message_preview',
        'approved_display',
        'date_created'
    ]
    list_filter = [
        'approved',
        'date_created',
        'project__category',
        'project__status'
    ]
    search_fields = [
        'name',
        'email',
        'message',
        'project__title'
    ]
    readonly_fields = [
        'id',
        'date_created',
        'project_link'
    ]
    raw_id_fields = ['project']
    
    fieldsets = (
        ('Comment Details', {
            'fields': ('name', 'email', 'message')
        }),
        ('Project', {
            'fields': ('project_link',),
            'classes': ('collapse',)
        }),
        ('Moderation', {
            'fields': ('approved',)
        }),
        ('Metadata', {
            'fields': ('id', 'date_created'),
            'classes': ('collapse',)
        }),
    )
    
    def project_title(self, obj):
        """Display project title with link"""
        if obj.project:
            url = reverse('admin:projects_project_change', args=[obj.project.pk])
            return format_html('<a href="{}">{}</a>', url, obj.project.title)
        return '-'
    project_title.short_description = 'Project'
    
    def message_preview(self, obj):
        """Show truncated message in list view"""
        return (obj.message[:75] + '...') if len(obj.message) > 75 else obj.message
    message_preview.short_description = 'Message Preview'
    
    def approved_display(self, obj):
        """Display approval status with color coding"""
        if obj.approved:
            return format_html('<span style="color: green;">✓ Approved</span>')
        return format_html('<span style="color: red;">✗ Pending</span>')
    approved_display.short_description = 'Status'
    
    def project_link(self, obj):
        """Link to parent project"""
        if obj.project:
            url = reverse('admin:projects_project_change', args=[obj.project.pk])
            return format_html('<a href="{}" target="_blank">{}</a>', url, obj.project.title)
        return '-'
    project_link.short_description = 'Project'
    
    actions = ['approve_comments', 'reject_comments', 'delete_spam']
    
    def approve_comments(self, request, queryset):
        """Approve selected comments"""
        updated = queryset.update(approved=True)
        self.message_user(request, f"Successfully approved {updated} comment(s).")
    approve_comments.short_description = "Approve selected comments"
    
    def reject_comments(self, request, queryset):
        """Reject selected comments"""
        updated = queryset.update(approved=False)
        self.message_user(request, f"Successfully rejected {updated} comment(s).")
    reject_comments.short_description = "Reject selected comments"
    
    def delete_spam(self, request, queryset):
        """Delete selected comments (for spam)"""
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"Successfully deleted {count} comment(s).")
    delete_spam.short_description = "Delete selected comments (spam)"
    
    def get_queryset(self, request):
        """Optimize queryset with related data"""
        return super().get_queryset(request).select_related('project').order_by('-date_created')


@admin.register(ProjectGalleryImage)
class ProjectGalleryImageAdmin(BaseAdminPermissions):
    """
    Admin interface for ProjectGalleryImage model
    """
    
    list_display = [
        'project_title',
        'image_preview',
        'alt_text',
        'sort_order',
        'id'
    ]
    list_filter = [
        'project__category',
        'project__status'
    ]
    search_fields = [
        'project__title',
        'alt_text'
    ]
    readonly_fields = ['image_preview']
    raw_id_fields = ['project']
    ordering = ['project', 'sort_order']
    
    fieldsets = (
        ('Image Details', {
            'fields': ('project', 'image_url', 'alt_text', 'sort_order')
        }),
        ('Preview', {
            'fields': ('image_preview',),
            'classes': ('collapse',)
        }),
    )
    
    def project_title(self, obj):
        """Display project title with link"""
        if obj.project:
            url = reverse('admin:projects_project_change', args=[obj.project.pk])
            return format_html('<a href="{}">{}</a>', url, obj.project.title)
        return '-'
    project_title.short_description = 'Project'
    
    def image_preview(self, obj):
        """Display image preview in admin"""
        if obj.image_url:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 120px; '
                'border: 1px solid #ddd; border-radius: 4px;" />',
                obj.image_url
            )
        return '-'
    image_preview.short_description = 'Image Preview'
    
    def get_queryset(self, request):
        """Optimize queryset with related data"""
        return super().get_queryset(request).select_related('project')


# Custom admin site configuration removed - now configured in settings.py via Jazzmin