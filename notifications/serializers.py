# notifications/serializers.py
from rest_framework import serializers
from django.utils.html import strip_tags
from .models import Message, MessageReply


class MessageReplySerializer(serializers.ModelSerializer):
    """Serializer for MessageReply model"""
    
    class Meta:
        model = MessageReply
        fields = ['id', 'message', 'sender_name', 'sender_type', 'reply_message', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate_reply_message(self, value):
        """Validate and clean reply message"""
        if len(value) > 1000:
            raise serializers.ValidationError('Reply message cannot exceed 1000 characters.')
        return strip_tags(value.strip())


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model - used in admin list/detail views"""
    
    class Meta:
        model = Message
        fields = [
            'id', 'sender_name', 'email', 'phone', 'subject', 'message',
            'status', 'message_type', 'order', 'ip_address', 'country', 'device',
            'assigned_to', 'user_id', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'ip_address', 
            'device', 'country', 'status', 'assigned_to', 'user_id'
        ]


class MessageDetailSerializer(serializers.ModelSerializer):
    """Serializer for Message model with replies - used in admin retrieve"""
    message_replies = MessageReplySerializer(many=True, read_only=True)
    word_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Message
        fields = [
            'id', 'sender_name', 'email', 'phone', 'subject', 'message', 'word_count',
            'status', 'message_type', 'order', 'ip_address', 'country', 'device',
            'assigned_to', 'user_id', 'message_replies',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'ip_address', 
            'device', 'country', 'status', 'assigned_to', 'user_id', 'word_count'
        ]


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


class OrderMessageSerializer(serializers.ModelSerializer):
    """Serializer for order messages - user-facing order communication"""
    message_replies = MessageReplySerializer(many=True, read_only=True)
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = [
            'id', 'sender_name', 'email', 'message', 'order',
            'message_replies', 'unread_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'unread_count']
    
    def get_unread_count(self, obj):
        """Count unread replies for the current user"""
        # TODO: Implement proper unread tracking with user FK on MessageReply
        # For now, return total reply count
        return obj.message_replies.count()
