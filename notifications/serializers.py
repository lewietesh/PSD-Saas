# notifications/serializers.py
from rest_framework import serializers
from django.utils.html import strip_tags
from .models import (
    ContactMessage, GeneralMessage, GeneralMessageAttachment,
    Message, MessageAttachment, Conversation
)
from accounts.serializers import UserBasicSerializer


# ==================== CONTACT MESSAGE SERIALIZERS ====================
class ContactMessageSerializer(serializers.ModelSerializer):
    """Serializer for ContactMessage (simple contact form)"""
    
    class Meta:
        model = ContactMessage
        fields = [
            'id', 'name', 'email', 'phone', 'subject', 'message',
            'source', 'is_read', 'replied', 'priority',
            'admin_reply', 'replied_by', 'replied_at', 'date_created'
        ]
        read_only_fields = ['id', 'is_read', 'replied', 'admin_reply', 'replied_by', 'replied_at', 'date_created']


class ContactMessageCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating contact messages (public form)"""
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message', 'source']


# ==================== GENERAL MESSAGE SERIALIZERS ====================
class GeneralMessageAttachmentSerializer(serializers.ModelSerializer):
    """Serializer for general message attachment"""
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = GeneralMessageAttachment
        fields = ['id', 'url', 'original_filename', 'file_size', 'uploaded_at']
        read_only_fields = ['id', 'file_size', 'uploaded_at']
    
    def get_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url if obj.file else None


class GeneralMessageSerializer(serializers.ModelSerializer):
    """Serializer for GeneralMessage (external inquiries with subjects)"""
    attachment = GeneralMessageAttachmentSerializer(read_only=True)
    attachment_file = serializers.FileField(write_only=True, required=False)
    assigned_to_name = serializers.CharField(source='assigned_to.email', read_only=True)
    replied_by_name = serializers.CharField(source='replied_by.email', read_only=True)
    
    class Meta:
        model = GeneralMessage
        fields = [
            'id', 'sender_name', 'email', 'phone', 'message', 'subject', 'status',
            'ip_address', 'country', 'device', 'assigned_to', 'assigned_to_name',
            'admin_reply', 'replied_by', 'replied_by_name', 'replied_at',
            'created_at', 'updated_at', 'attachment', 'attachment_file'
        ]
        read_only_fields = [
            'id', 'ip_address', 'country', 'device', 'admin_reply', 
            'replied_by', 'replied_at', 'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        attachment_file = validated_data.pop('attachment_file', None)
        general_message = GeneralMessage.objects.create(**validated_data)
        
        # Create attachment if provided
        if attachment_file:
            GeneralMessageAttachment.objects.create(
                general_message=general_message,
                file=attachment_file,
                original_filename=attachment_file.name,
                file_size=attachment_file.size
            )
        
        return general_message


class GeneralMessageCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating general messages (public form)"""
    attachment_file = serializers.FileField(required=False)
    
    class Meta:
        model = GeneralMessage
        fields = ['sender_name', 'email', 'phone', 'message', 'subject', 'attachment_file']


# ==================== MESSAGE SERIALIZERS (In-System Users) ====================
class MessageAttachmentSerializer(serializers.ModelSerializer):
    """Serializer for message attachments"""
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = MessageAttachment
        fields = ['id', 'url', 'original_filename', 'file_size', 'uploaded_at']
        read_only_fields = ['id', 'file_size', 'uploaded_at']
    
    def get_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url if obj.file else None


# ==================== CONVERSATION SERIALIZER ====================
class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for conversation threads"""
    
    unread_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Conversation
        fields = [
            'id', 'conversation_type', 'title', 'status',
            'user', 'user_email', 'order', 'order_number',
            'unread_count', 'last_message',
            'created_at', 'updated_at', 'last_message_at'
        ]
        read_only_fields = ['id', 'user', 'order', 'created_at', 'updated_at', 'last_message_at']
    
    def get_unread_count(self, obj):
        return obj.unread_count
    
    def get_last_message(self, obj):
        last_msg = obj.messages.order_by('-created_at').first()
        if last_msg:
            return {
                'id': str(last_msg.id),
                'content': last_msg.content[:100] + '...' if len(last_msg.content) > 100 else last_msg.content,
                'sender': last_msg.sender,
                'created_at': last_msg.created_at.isoformat()
            }
        return None


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for in-system user messages"""
    attachments = MessageAttachmentSerializer(many=True, read_only=True)
    # NOTE: 'replies' field removed - support replies are now Message records with sender='support'
    # All messages in a conversation (user and support) are returned together
    attachment_files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )
    user_email = serializers.EmailField(source='user.email', read_only=True)
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    sender_name = serializers.SerializerMethodField()
    sender_avatar = serializers.SerializerMethodField()
    # Expose conversation UUID as conversation_id for frontend compatibility
    conversation_id = serializers.CharField(source='conversation.id', read_only=True)
    
    class Meta:
        model = Message
        fields = [
            'id', 'conversation', 'conversation_id',
            'message_type', 'sender', 'sender_name', 'sender_avatar',
            'user', 'user_email', 'order', 'order_number',
            'content', 'is_read', 'created_at', 'updated_at',
            'attachments', 'attachment_files'
        ]
        read_only_fields = ['id', 'user', 'sender', 'conversation', 'conversation_id', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validate that order is provided for order messages"""
        message_type = data.get('message_type', 'general')
        order = data.get('order')
        
        if message_type == 'order' and not order:
            raise serializers.ValidationError({
                'order': 'Order is required for order-type messages.'
            })
        
        return data
    
    def get_sender_name(self, obj):
        """Get display name for message sender"""
        if obj.sender == 'system':
            return 'System'
        elif obj.sender == 'support':
            return 'Support Team'
        elif obj.user:
            # Get user's full name or email
            full_name = f"{obj.user.first_name} {obj.user.last_name}".strip()
            return full_name if full_name else obj.user.email.split('@')[0]
        return 'User'
    
    def get_sender_avatar(self, obj):
        """Get avatar URL for sender"""
        if obj.user and obj.user.profile_img:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.user.profile_img.url)
        return None
    
    def create(self, validated_data):
        attachment_files = validated_data.pop('attachment_files', [])
        message = Message.objects.create(**validated_data)
        
        # Create attachments
        for file in attachment_files:
            MessageAttachment.objects.create(
                message=message,
                file=file,
                original_filename=file.name,
                file_size=file.size
            )
        
        return message


class MessageListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing messages"""
    attachments_count = serializers.IntegerField(source='attachments.count', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    sender_name = serializers.SerializerMethodField()
    sender_avatar = serializers.SerializerMethodField()
    # Expose conversation UUID as conversation_id for frontend compatibility
    conversation_id = serializers.CharField(source='conversation.id', read_only=True)
    
    class Meta:
        model = Message
        fields = [
            'id', 'conversation_id', 'message_type', 'sender', 'sender_name', 'sender_avatar',
            'user_email', 'content', 'is_read', 'created_at',
            'attachments_count'
        ]
        read_only_fields = fields
    
    def get_sender_name(self, obj):
        """Get display name for message sender"""
        if obj.sender == 'system':
            return 'System'
        elif obj.sender == 'support':
            return 'Support Team'
        elif obj.user:
            full_name = f"{obj.user.first_name} {obj.user.last_name}".strip()
            return full_name if full_name else obj.user.email.split('@')[0]
        return 'User'
    
    def get_sender_avatar(self, obj):
        """Get avatar URL for sender"""
        if obj.user and obj.user.profile_img:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.user.profile_img.url)
        return None


# ==================== ANONYMOUS MESSAGE SERIALIZER ====================
class AnonymousMessageSerializer(serializers.ModelSerializer):
    """
    Serializer for anonymous chat messages
    Simplified - no file attachments, limited fields exposed
    """
    sender_name = serializers.SerializerMethodField()
    sender_avatar = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = [
            'id', 'content', 'sender', 'sender_name', 'sender_avatar',
            'is_read', 'created_at'
        ]
        read_only_fields = ['id', 'sender', 'is_read', 'created_at']
    
    def get_sender_name(self, obj):
        """Get display name for message sender"""
        if obj.sender == 'support':
            return 'Support Team'
        elif obj.sender == 'system':
            return 'System'
        return 'You'  # Anonymous user sees themselves as 'You'
    
    def get_sender_avatar(self, obj):
        """Get avatar URL for sender - only support has avatar"""
        # For anonymous chat, we don't expose user avatars
        # Could return a default support avatar here
        return None


class PublicMessageSerializer(serializers.ModelSerializer):
    """Serializer for public message submission (frontend contact form)"""
    
    class Meta:
        model = Message
        fields = ['sender_name', 'email', 'phone', 'subject', 'message']
    
    def validate_sender_name(self, value):
        """Validate sender name format"""
        cleaned = value.strip()
        if len(cleaned) < 2:
            raise serializers.ValidationError('Name must be at least 2 characters long.')
        # Basic sanitization - remove any HTML tags
        return strip_tags(cleaned)
    
    def validate_message(self, value):
        """Validate and sanitize message content"""
        # Strip HTML tags for security
        cleaned = strip_tags(value.strip())
        
        if len(cleaned) < 10:
            raise serializers.ValidationError('Message must be at least 10 characters long.')
        
        # Word count validation (max 500 words)
        word_count = len(cleaned.split())
        if word_count > 500:
            raise serializers.ValidationError(
                f'Message exceeds 500 words (currently {word_count} words). Please shorten your message.'
            )
        
        return cleaned
    
    def validate_email(self, value):
        """Basic email validation"""
        return value.lower().strip()
    
    def validate_phone(self, value):
        """Clean phone number"""
        if value:
            return strip_tags(value.strip())
        return value
