# notifications/admin.py
from django.contrib import admin
from django.utils.html import format_html
from accounts.admin import BaseAdminPermissions
from .models import Message, MessageReply


class MessageReplyInline(admin.TabularInline):
    """Inline for adding replies to messages"""
    model = MessageReply
    fields = ['sender_name', 'sender_type', 'reply_message', 'created_at']
    readonly_fields = ['created_at']
    extra = 1
    can_delete = True


@admin.register(Message)
class MessageAdmin(BaseAdminPermissions):
    """Admin interface for Message model"""
    
    list_display = [
        'sender_name', 'email', 'subject', 'message_type', 'order_link',
        'status', 'message_preview', 'assigned_to', 'replies_count', 'created_at'
    ]
    list_filter = ['status', 'subject', 'message_type', 'assigned_to', 'created_at']
    search_fields = ['sender_name', 'email', 'message', 'id', 'order__id']
    readonly_fields = [
        'id', 'sender_name', 'email', 'phone', 'message',
        'ip_address', 'country', 'device', 'user_id', 'message_type',
        'created_at', 'updated_at', 'device_info_display', 'order_link'
    ]
    
    fields = [
        ('sender_name', 'email'),
        'phone',
        ('subject', 'message_type'),
        'message',
        ('status', 'assigned_to'),
        'user_id',
        'order_link',
        ('ip_address', 'country'),
        'device_info_display',
        ('created_at', 'updated_at')
    ]
    
    inlines = [MessageReplyInline]
    
    ordering = ['-created_at']
    
    actions = ['mark_as_lead', 'mark_as_client', 'mark_as_closed', 'assign_to_me']
    
    def order_link(self, obj):
        """Display link to related order if exists"""
        if obj.order:
            from django.urls import reverse
            from django.utils.html import format_html
            url = reverse('admin:business_order_change', args=[obj.order.id])
            return format_html('<a href="{}" target="_blank">Order #{}</a>', url, str(obj.order.id)[:8])
        return '-'
    order_link.short_description = 'Related Order'
    
    def message_preview(self, obj):
        """Show truncated message preview"""
        if obj.message:
            preview = obj.message[:75] + '...' if len(obj.message) > 75 else obj.message
            return preview
        return '-'
    message_preview.short_description = 'Message Preview'
    
    def replies_count(self, obj):
        """Count number of replies"""
        count = obj.message_replies.count()
        if count > 0:
            return format_html('<span style="color: green; font-weight: bold;">{}</span>', count)
        return count
    replies_count.short_description = 'Replies'
    
    def device_info_display(self, obj):
        """Display formatted device info"""
        if obj.device:
            # Truncate long user agent strings
            device_str = obj.device[:100] + '...' if len(obj.device) > 100 else obj.device
            return format_html('<span style="font-size: 11px; font-family: monospace;">{}</span>', device_str)
        return 'Not captured'
    device_info_display.short_description = 'Device Info'
    
    def mark_as_lead(self, request, queryset):
        """Mark selected messages as lead"""
        count = queryset.update(status='lead')
        self.message_user(request, f'{count} message(s) marked as lead.')
    mark_as_lead.short_description = 'Mark as Lead'
    
    def mark_as_client(self, request, queryset):
        """Mark selected messages as client"""
        count = queryset.update(status='client')
        self.message_user(request, f'{count} message(s) marked as client.')
    mark_as_client.short_description = 'Mark as Client'
    
    def mark_as_closed(self, request, queryset):
        """Mark selected messages as closed"""
        count = queryset.update(status='closed')
        self.message_user(request, f'{count} message(s) marked as closed.')
    mark_as_closed.short_description = 'Mark as Closed'
    
    def assign_to_me(self, request, queryset):
        """Assign selected messages to current admin"""
        count = queryset.update(assigned_to=request.user)
        self.message_user(request, f'{count} message(s) assigned to you.')
    assign_to_me.short_description = 'Assign to Me'


@admin.register(MessageReply)
class MessageReplyAdmin(BaseAdminPermissions):
    """Admin interface for MessageReply model"""
    
    list_display = ['sender_name', 'sender_type', 'message', 'created_at']
    list_filter = ['sender_type', 'created_at']
    search_fields = ['sender_name', 'reply_message', 'message__sender_name']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
