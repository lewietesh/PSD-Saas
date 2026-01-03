# notifications/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django import forms
from accounts.admin import BaseAdminPermissions
from .models import (
    ContactMessage, GeneralMessage, GeneralMessageAttachment,
    Message, MessageAttachment, Conversation
)


# ==================== CONTACT MESSAGE ADMIN ====================
@admin.register(ContactMessage)
class ContactMessageAdmin(BaseAdminPermissions):
    """Admin for simple contact form submissions"""
    list_display = ('id', 'name', 'email', 'subject', 'priority', 'source', 'is_read', 'replied', 'date_created')
    list_filter = ('priority', 'source', 'is_read', 'replied', 'date_created')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('id', 'date_created', 'replied_at')
    ordering = ('-date_created',)
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('Tracking', {
            'fields': ('source', 'priority', 'is_read', 'replied')
        }),
        ('Admin Reply', {
            'fields': ('admin_reply', 'replied_by', 'replied_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('date_created',),
            'classes': ('collapse',)
        }),
    )


# ==================== GENERAL MESSAGE ADMIN ====================
class GeneralMessageAttachmentInline(admin.StackedInline):
    """Inline for single attachment on general message"""
    model = GeneralMessageAttachment
    max_num = 1
    extra = 0
    readonly_fields = ('original_filename', 'file_size', 'uploaded_at')
    fields = ('file', 'original_filename', 'file_size', 'uploaded_at')


@admin.register(GeneralMessage)
class GeneralMessageAdmin(BaseAdminPermissions):
    """Admin for general inquiry messages with subject categorization"""
    
    list_display = [
        'sender_name', 'email', 'subject', 'status', 'message_preview', 
        'assigned_to', 'has_attachment', 'has_reply', 'created_at'
    ]
    list_filter = ['status', 'subject', 'assigned_to', 'created_at']
    search_fields = ['sender_name', 'email', 'message', 'id']
    readonly_fields = [
        'id', 'created_at', 'updated_at', 'ip_address', 'country', 'device', 'replied_at'
    ]
    
    fieldsets = (
        ('Sender Information', {
            'fields': ('sender_name', 'email', 'phone')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('Status & Assignment', {
            'fields': ('status', 'assigned_to')
        }),
        ('Admin Reply (One Reply Only)', {
            'fields': ('admin_reply', 'replied_by', 'replied_at'),
            'classes': ('collapse',)
        }),
        ('Tracking Info', {
            'fields': ('ip_address', 'country', 'device'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [GeneralMessageAttachmentInline]
    ordering = ['-created_at']
    actions = ['mark_as_lead', 'mark_as_client', 'mark_as_closed', 'assign_to_me']
    
    def message_preview(self, obj):
        """Show first 50 characters of message"""
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'
    
    def has_attachment(self, obj):
        """Check if message has attachment"""
        try:
            return bool(obj.attachment)
        except GeneralMessageAttachment.DoesNotExist:
            return False
    has_attachment.boolean = True
    has_attachment.short_description = 'Attachment'
    
    def has_reply(self, obj):
        """Check if admin has replied"""
        return bool(obj.admin_reply)
    has_reply.boolean = True
    has_reply.short_description = 'Replied'
    
    def mark_as_lead(self, request, queryset):
        count = queryset.update(status='lead')
        self.message_user(request, f'{count} messages marked as leads.')
    mark_as_lead.short_description = "Mark as Lead"
    
    def mark_as_client(self, request, queryset):
        count = queryset.update(status='client')
        self.message_user(request, f'{count} messages marked as clients.')
    mark_as_client.short_description = "Mark as Client"
    
    def mark_as_closed(self, request, queryset):
        count = queryset.update(status='closed')
        self.message_user(request, f'{count} messages marked as closed.')
    mark_as_closed.short_description = "Mark as Closed"
    
    def assign_to_me(self, request, queryset):
        count = queryset.update(assigned_to=request.user)
        self.message_user(request, f'{count} messages assigned to you.')
    assign_to_me.short_description = "Assign to Me"


# ==================== IN-SYSTEM MESSAGE ADMIN ====================
# NOTE: MessageReplyInline has been removed - support replies are now Message records with sender='support'
# All messages (user and support) are stored in the same Conversation thread


class MessageAttachmentInline(admin.TabularInline):
    """Inline for message attachments"""
    model = MessageAttachment
    fields = ['file', 'original_filename', 'file_size_kb', 'uploaded_at']
    readonly_fields = ['original_filename', 'file_size_kb', 'uploaded_at']
    extra = 0
    can_delete = True
    
    def file_size_kb(self, obj):
        """Display file size in KB"""
        if obj.file_size:
            if obj.file_size < 1024 * 1024:
                return f"{obj.file_size / 1024:.2f} KB"
            return f"{obj.file_size / (1024 * 1024):.2f} MB"
        return '-'
    file_size_kb.short_description = 'File Size'


# ==================== CONVERSATION ADMIN ====================
@admin.register(Conversation)
class ConversationAdmin(BaseAdminPermissions):
    """Admin interface for conversation threads"""
    
    list_display = [
        'conversation_type', 'title', 'user_or_session', 'order_link',
        'status', 'message_count', 'unread_count_display', 'last_message_at', 'created_at', 'view_conversation_link'
    ]
    list_filter = ['conversation_type', 'status', 'created_at', 'last_message_at']
    search_fields = ['title', 'user__email', 'order__order_number', 'session_id']
    readonly_fields = ['created_at', 'updated_at', 'last_message_at', 'session_id', 'ip_address']
    ordering = ['-last_message_at', '-created_at']
    raw_id_fields = ['user', 'order']
    
    fieldsets = (
        ('Conversation Info', {
            'fields': ('conversation_type', 'title', 'status')
        }),
        ('Relationships', {
            'fields': ('user', 'order')
        }),
        ('Anonymous Info', {
            'fields': ('session_id', 'ip_address'),
            'classes': ('collapse',),
            'description': 'Session info for anonymous conversations'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'last_message_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_or_session(self, obj):
        """Display user email or session ID for anonymous conversations"""
        if obj.user:
            return obj.user.email
        elif obj.session_id:
            # Show truncated session ID for anonymous users
            return format_html(
                '<span style="color: #888; font-style: italic;" title="{}">Anonymous ({}...)</span>',
                obj.session_id,
                obj.session_id[:8]
            )
        return '-'
    user_or_session.short_description = 'User / Session'
    user_or_session.admin_order_field = 'user__email'
    
    def order_link(self, obj):
        if obj.order:
            url = reverse('admin:business_order_change', args=[obj.order.id])
            return format_html('<a href="{}">{}</a>', url, obj.order.order_number)
        return '-'
    order_link.short_description = 'Order'
    
    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Messages'
    
    def unread_count_display(self, obj):
        count = obj.unread_count
        if count > 0:
            return format_html('<span style="color: red; font-weight: bold;">{}</span>', count)
        return '0'
    unread_count_display.short_description = 'Unread'
    
    def view_conversation_link(self, obj):
        """Display a link to view the full conversation (goes to first message)"""
        first_message = obj.messages.first()
        if first_message:
            url = reverse('admin:notifications_message_change', args=[first_message.id])
            return format_html(
                '<a href="{}" class="button" style="padding: 4px 8px; background: #417690; color: white; '
                'text-decoration: none; border-radius: 4px; font-size: 11px;">View Chat</a>',
                url
            )
        return '-'
    view_conversation_link.short_description = 'Actions'


@admin.register(Message)
class MessageAdmin(BaseAdminPermissions):
    """Admin interface for in-system user messages - Chat-style view"""
    change_form_template = 'admin/notifications/message/change_form.html'
    
    list_display = [
        'user_display', 'conversation_link', 'message_type', 'content_preview', 'replies_count', 
        'attachments_count', 'is_read', 'created_at'
    ]
    list_filter = ['message_type', 'sender', 'is_read', 'created_at', 'user', 'conversation__conversation_type']
    search_fields = ['content', 'user__email', 'order__id', 'conversation__id', 'id']
    readonly_fields = [
        'id', 'created_at', 'updated_at', 'conversation_display', 
        'user_info', 'message_details_display', 'attachment_summary'
    ]
    
    fieldsets = (
        (None, {
            'fields': ('conversation_display',),
        }),
        (None, {
            'fields': ('user_info', 'message_details_display', 'attachment_summary'),
        }),
    )
    
    # Only keep MessageAttachmentInline - reply form is now in template
    inlines = [MessageAttachmentInline]
    ordering = ['-created_at']
    actions = ['mark_as_read', 'mark_as_unread']
    
    def user_display(self, obj):
        """Display user email WITHOUT clickable link"""
        if obj.user:
            return obj.user.email
        return '-'
    user_display.short_description = 'User'
    user_display.admin_order_field = 'user__email'
    
    def conversation_link(self, obj):
        """Display conversation with link to conversation admin"""
        if obj.conversation:
            url = reverse('admin:notifications_conversation_change', args=[obj.conversation.id])
            return format_html('<a href="{}">{}</a>', url, obj.conversation.title or str(obj.conversation.id)[:8])
        return '-'
    conversation_link.short_description = 'Conversation'
    conversation_link.admin_order_field = 'conversation'
    
    def conversation_display(self, obj):
        """Display the entire conversation in a chat-like format"""
        # Get all messages in this conversation (both user and support)
        from .models import Message
        conversation_messages = Message.objects.filter(
            conversation=obj.conversation
        ).select_related('user', 'order').order_by('created_at')
        
        # Original message timestamp
        timestamp = obj.created_at.strftime('%b %d, %Y %I:%M %p')
        sender_name = obj.user.email if obj.user else 'User'
        
        # Create reply URL - use custom view
        reply_url = reverse('admin_reply_to_message', args=[obj.id])
        
        # Conversation info header
        conversation_info = ''
        if obj.message_type == 'order' and obj.order:
            conversation_info = f'<span style="background: #e3f2fd; color: #1976d2; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 600;">📦 Order #{obj.order.id[:8]}...</span>'
        else:
            conversation_info = f'<span style="background: #f3e5f5; color: #7b1fa2; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 600;">💬 General Support</span>'
        
        conv_title = obj.conversation.title if obj.conversation else 'Unknown'
        conv_id = str(obj.conversation.id)[:12] if obj.conversation else 'N/A'
        
        html = f'''
        <div style="background: #fafafa; padding: 20px; border-radius: 8px; margin-bottom: 20px; border: 2px solid #e0e0e0;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 20px; margin: -20px -20px 20px -20px; border-radius: 6px 6px 0 0; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3 style="margin: 0; font-size: 18px;">💬 {conv_title}</h3>
                    <p style="margin: 5px 0 0 0; font-size: 13px; opacity: 0.9;">{conversation_info} • {conversation_messages.count()} message(s) in this conversation</p>
                </div>
                <a href="{reply_url}" style="background: white; color: #667eea; padding: 10px 20px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 14px;">
                    ✍️ Reply to Message
                </a>
            </div>
            
            <!-- All Messages in Conversation -->
        '''
        
        for idx, msg in enumerate(conversation_messages):
            msg_timestamp = msg.created_at.strftime('%b %d, %Y %I:%M %p')
            msg_sender = msg.user.email if msg.user else 'User'
            is_current = msg.id == obj.id
            
            border_style = 'border-left: 5px solid #667eea;' if is_current else 'border-left: 5px solid #ddd;'
            bg_color = '#fff' if is_current else '#f9f9f9'
            
            html += f'''
            <div style="margin: 15px 0;">
                <div style="background: {bg_color}; padding: 18px 22px; border-radius: 12px; {border_style} box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                        <div style="background: #667eea; color: white; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; margin-right: 12px;">
                            {'🛡️' if msg.sender == 'support' else '👤'}
                        </div>
                        <div>
                            <div style="font-weight: bold; color: #667eea; font-size: 15px;">
                                {msg_sender} {'<span style="background: #4caf50; color: white; padding: 2px 8px; border-radius: 10px; font-size: 11px; margin-left: 6px;">CURRENT</span>' if is_current else ''}
                            </div>
                            <div style="font-size: 12px; color: #666;">
                                {msg_timestamp} • {msg.get_sender_display()}
                            </div>
                        </div>
                    </div>
                    <div style="white-space: pre-wrap; word-wrap: break-word; line-height: 1.6; color: #333; font-size: 14px;">
                        {msg.content}
                    </div>
                </div>
            </div>
            '''
        
        # NOTE: MessageReply display removed - all messages (user and support) are now 
        # shown as Message records in the conversation loop above
        
        html += '</div>'
        return format_html(html)
    conversation_display.short_description = 'Conversation'
    
    def user_info(self, obj):
        """Display formatted user information with link to view profile"""
        if obj.user:
            user_url = reverse('admin:accounts_user_change', args=[obj.user.id])
            html = f'''
            <div style="background: #f5f5f5; padding: 12px; border-radius: 6px;">
                <strong>Email:</strong> {obj.user.email}<br>
                <strong>Name:</strong> {obj.user.get_full_name() or 'N/A'}<br>
                <strong>User ID:</strong> {str(obj.user.id)[:8]}<br>
                <div style="margin-top: 8px;">
                    <a href="{user_url}" target="_blank" style="padding: 6px 12px; background: #666; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">
                        👤 View Full Profile
                    </a>
                </div>
            </div>
            '''
            return format_html(html)
        return '-'
    user_info.short_description = 'User Details'
    
    def message_details_display(self, obj):
        """Display formatted message details"""
        html = '''
        <div style="background: #f5f5f5; padding: 15px; border-radius: 6px; margin-top: 10px;">
            <h4 style="margin-top: 0; color: #1976d2; border-bottom: 2px solid #1976d2; padding-bottom: 8px;">
                📋 Message Details
            </h4>
        '''
        
        # Message Type
        html += f'''
            <div style="margin: 10px 0; padding: 8px; background: white; border-radius: 4px;">
                <strong>Type:</strong> 
                <span style="background: #2196f3; color: white; padding: 4px 10px; border-radius: 12px; font-size: 13px;">
                    {obj.get_message_type_display()}
                </span>
            </div>
        '''
        
        # Read Status
        read_status = '✅ Read' if obj.is_read else '⭕ Unread'
        read_color = '#4caf50' if obj.is_read else '#ff9800'
        html += f'''
            <div style="margin: 10px 0; padding: 8px; background: white; border-radius: 4px;">
                <strong>Status:</strong> 
                <span style="background: {read_color}; color: white; padding: 4px 10px; border-radius: 12px; font-size: 13px;">
                    {read_status}
                </span>
            </div>
        '''
        
        # Order Link
        if obj.order:
            order_url = reverse('admin:business_order_change', args=[obj.order.id])
            html += f'''
            <div style="margin: 10px 0; padding: 8px; background: white; border-radius: 4px;">
                <strong>Related Order:</strong><br>
                <a href="{order_url}" target="_blank" style="margin-top: 5px; display: inline-block; padding: 6px 12px; background: #1976d2; color: white; text-decoration: none; border-radius: 4px; font-size: 13px;">
                    📦 View Order #{str(obj.order.id)[:8]}
                </a>
            </div>
            '''
        else:
            html += '''
            <div style="margin: 10px 0; padding: 8px; background: white; border-radius: 4px;">
                <strong>Related Order:</strong> 
                <span style="color: #999;">No order linked</span>
            </div>
            '''
        
        # Timestamps
        html += f'''
            <div style="margin: 10px 0; padding: 8px; background: white; border-radius: 4px;">
                <strong>Created:</strong> {obj.created_at.strftime('%b %d, %Y at %I:%M %p')}<br>
                <strong>Last Updated:</strong> {obj.updated_at.strftime('%b %d, %Y at %I:%M %p')}
            </div>
        '''
        
        html += '</div>'
        return format_html(html)
    message_details_display.short_description = 'Message Information'
    
    def order_link(self, obj):
        """Link to related order"""
        if obj.order:
            url = reverse('admin:business_order_change', args=[obj.order.id])
            return format_html(
                '<a href="{}" style="padding: 8px 12px; background: #1976d2; color: white; text-decoration: none; border-radius: 4px; display: inline-block;">📦 View Order #{}</a>', 
                url, str(obj.order.id)[:8]
            )
        return format_html('<span style="color: #999;">No order linked</span>')
    order_link.short_description = 'Related Order'
    
    def attachment_summary(self, obj):
        """Display attachment summary with clear message if none exist"""
        attachments = obj.attachments.all()
        
        html = '''
        <div style="background: #f5f5f5; padding: 15px; border-radius: 6px; margin-top: 10px;">
            <h4 style="margin-top: 0; color: #1976d2; border-bottom: 2px solid #1976d2; padding-bottom: 8px;">
                📎 Attachments
            </h4>
        '''
        
        if attachments.exists():
            html += f'<p style="margin: 10px 0;"><strong>{attachments.count()} File(s) Attached:</strong></p>'
            html += '<ul style="margin: 8px 0; padding-left: 20px; list-style: none;">'
            for att in attachments:
                if att.file_size < 1024 * 1024:
                    size = f"{att.file_size / 1024:.2f} KB"
                else:
                    size = f"{att.file_size / (1024 * 1024):.2f} MB"
                
                file_url = att.file.url if att.file else '#'
                html += f'''
                <li style="margin: 8px 0; padding: 10px; background: white; border-radius: 4px; border-left: 4px solid #2196f3;">
                    <strong>📄 {att.original_filename}</strong><br>
                    <small style="color: #666;">Size: {size}</small><br>
                    <a href="{file_url}" target="_blank" style="margin-top: 5px; display: inline-block; padding: 4px 10px; background: #2196f3; color: white; text-decoration: none; border-radius: 3px; font-size: 12px;">
                        Download
                    </a>
                </li>
                '''
            html += '</ul>'
        else:
            html += '''
            <div style="padding: 20px; background: #fff3cd; border-radius: 6px; text-align: center; border: 2px dashed #ffc107;">
                <div style="font-size: 32px; margin-bottom: 8px;">📭</div>
                <strong style="color: #856404;">No attachments</strong><br>
                <small style="color: #856404;">This message has no file attachments</small>
            </div>
            '''
        
        html += '</div>'
        return format_html(html)
    attachment_summary.short_description = 'File Attachments'
    
    def content_preview(self, obj):
        """Show first 60 characters of content"""
        return obj.content[:60] + '...' if len(obj.content) > 60 else obj.content
    content_preview.short_description = 'Message'
    
    def replies_count(self, obj):
        """Count of support replies in the same conversation"""
        if obj.conversation:
            count = Message.objects.filter(
                conversation=obj.conversation,
                sender='support'
            ).count()
            if count > 0:
                return format_html('<span style="background: #4caf50; color: white; padding: 3px 8px; border-radius: 12px; font-weight: bold;">{}</span>', count)
        return format_html('<span style="color: #999;">0</span>')
    replies_count.short_description = 'Replies'
    
    def attachments_count(self, obj):
        """Count of attachments"""
        count = obj.attachments.count()
        if count > 0:
            return format_html('<span style="background: #2196f3; color: white; padding: 3px 8px; border-radius: 12px;">📎 {}</span>', count)
        return format_html('<span style="color: #999;">0</span>')
    attachments_count.short_description = 'Files'
    
    def mark_as_read(self, request, queryset):
        count = queryset.update(is_read=True)
        self.message_user(request, f'{count} message(s) marked as read.')
    mark_as_read.short_description = '✓ Mark as read'
    
    def mark_as_unread(self, request, queryset):
        count = queryset.update(is_read=False)
        self.message_user(request, f'{count} message(s) marked as unread.')
    mark_as_unread.short_description = '✗ Mark as unread'


@admin.register(MessageAttachment)
class MessageAttachmentAdmin(BaseAdminPermissions):
    """Admin for message attachments"""
    list_display = ['id_short', 'message_id_short', 'original_filename', 'file_size_display', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['original_filename', 'message__id']
    readonly_fields = ['id', 'original_filename', 'file_size', 'uploaded_at', 'message_link']
    
    fieldsets = (
        ('Attachment Info', {
            'fields': ('id', 'message_link', 'file', 'original_filename')
        }),
        ('File Details', {
            'fields': ('file_size', 'uploaded_at')
        }),
    )
    
    def id_short(self, obj):
        return str(obj.id)[:8]
    id_short.short_description = 'ID'
    
    def message_id_short(self, obj):
        return str(obj.message.id)[:8]
    message_id_short.short_description = 'Message ID'
    
    def file_size_display(self, obj):
        """Display file size in KB or MB"""
        if obj.file_size < 1024 * 1024:
            return f"{obj.file_size / 1024:.2f} KB"
        return f"{obj.file_size / (1024 * 1024):.2f} MB"
    file_size_display.short_description = 'Size'
    
    def message_link(self, obj):
        """Link to parent message"""
        url = reverse('admin:notifications_message_change', args=[obj.message.id])
        return format_html('<a href="{}">View Message: {}</a>', url, str(obj.message.id)[:8])
    message_link.short_description = 'Parent Message'
