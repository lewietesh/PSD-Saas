# notifications/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from rest_framework.throttling import AnonRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q, Count, Exists, OuterRef

from .models import (
    ContactMessage, GeneralMessage, GeneralMessageAttachment,
    Message, MessageAttachment, Conversation
)
from .serializers import (
    ContactMessageSerializer, ContactMessageCreateSerializer,
    GeneralMessageSerializer, GeneralMessageCreateSerializer,
    MessageSerializer, MessageListSerializer,
    MessageAttachmentSerializer, AnonymousMessageSerializer
)
from accounts.permissions import IsDeveloperOrAdmin
from emails.base import BaseEmail


# Custom throttle classes for anonymous chat
class AnonChatReadThrottle(AnonRateThrottle):
    """Throttle for reading anonymous chat messages (more permissive)"""
    scope = 'anon_chat_read'
    
    def get_cache_key(self, request, view):
        """Use session_id + IP for throttling"""
        session_id = request.query_params.get('session_id', '')
        ip = self.get_ident(request)
        return f'throttle_anon_chat_read_{session_id}_{ip}'


class AnonChatWriteThrottle(AnonRateThrottle):
    """Throttle for sending anonymous chat messages (stricter to prevent spam)"""
    scope = 'anon_chat_write'
    
    def get_cache_key(self, request, view):
        """Use session_id + IP for throttling"""
        session_id = request.data.get('session_id', '')
        ip = self.get_ident(request)
        return f'throttle_anon_chat_write_{session_id}_{ip}'


# ==================== CONTACT MESSAGE VIEWSET ====================
class ContactMessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing simple contact form submissions
    Public can create, only admins can view/manage
    """
    queryset = ContactMessage.objects.all().order_by('-date_created')
    serializer_class = ContactMessageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_read', 'replied', 'priority', 'source']
    
    def get_permissions(self):
        """Allow anyone to create, admin for everything else"""
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [IsDeveloperOrAdmin()]
    
    def get_serializer_class(self):
        """Use create serializer for POST"""
        if self.action == 'create':
            return ContactMessageCreateSerializer
        return ContactMessageSerializer
    
    def perform_create(self, serializer):
        """Create and send email notification"""
        instance = serializer.save()
        # Send email notification to admin
        send_new_message_notification(instance)
    
    @action(detail=True, methods=['post'], permission_classes=[IsDeveloperOrAdmin])
    def reply(self, request, pk=None):
        """Admin reply to contact message"""
        contact_message = self.get_object()
        admin_reply = request.data.get('admin_reply', '').strip()
        
        if not admin_reply:
            return Response(
                {'error': 'Reply cannot be empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        contact_message.admin_reply = admin_reply
        contact_message.replied = True
        contact_message.replied_by = request.user
        contact_message.replied_at = timezone.now()
        contact_message.save()
        
        serializer = self.get_serializer(contact_message)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsDeveloperOrAdmin])
    def mark_read(self, request):
        """Mark multiple messages as read"""
        ids = request.data.get('ids', [])
        if not ids:
            return Response(
                {'error': 'ids list required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        count = ContactMessage.objects.filter(id__in=ids).update(is_read=True)
        return Response({'count': count})


# ==================== GENERAL MESSAGE VIEWSET ====================
class GeneralMessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing general inquiry messages with file attachments
    Public can create, only admins can view/manage
    """
    queryset = GeneralMessage.objects.all().order_by('-created_at')
    serializer_class = GeneralMessageSerializer
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'subject', 'assigned_to']
    
    def get_permissions(self):
        """Allow anyone to create, admin for everything else"""
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [IsDeveloperOrAdmin()]
    
    def get_serializer_class(self):
        """Use create serializer for POST"""
        if self.action == 'create':
            return GeneralMessageCreateSerializer
        return GeneralMessageSerializer
    
    def perform_create(self, serializer):
        """Capture IP and device info when creating, send email notification"""
        request = self.request
        ip_address = request.META.get('REMOTE_ADDR')
        device = request.META.get('HTTP_USER_AGENT', '')
        
        instance = serializer.save(
            ip_address=ip_address,
            device=device[:255] if device else ''
        )
        # Send email notification to admin
        send_new_message_notification(instance)
    
    @action(detail=True, methods=['post'], permission_classes=[IsDeveloperOrAdmin])
    def reply(self, request, pk=None):
        """Admin reply to general message (one reply only)"""
        general_message = self.get_object()
        
        if general_message.admin_reply:
            return Response(
                {'error': 'This message has already been replied to'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        admin_reply = request.data.get('admin_reply', '').strip()
        if not admin_reply:
            return Response(
                {'error': 'Reply cannot be empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        general_message.admin_reply = admin_reply
        general_message.replied_by = request.user
        general_message.replied_at = timezone.now()
        general_message.save()
        
        serializer = self.get_serializer(general_message)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'], permission_classes=[IsDeveloperOrAdmin])
    def assign(self, request, pk=None):
        """Assign message to an admin"""
        general_message = self.get_object()
        assigned_to_id = request.data.get('assigned_to')
        
        if not assigned_to_id:
            general_message.assigned_to = None
        else:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                user = User.objects.get(id=assigned_to_id)
                general_message.assigned_to = user
            except User.DoesNotExist:
                return Response(
                    {'error': 'User not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        general_message.save()
        serializer = self.get_serializer(general_message)
        return Response(serializer.data)


# ==================== MESSAGE VIEWSET (In-System Users) ====================
class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for authenticated user messages (order and general support)
    Both user and support messages are Message records with different sender values
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    
    def get_queryset(self):
        """Filter messages by authenticated user and conversation context"""
        from .models import Conversation
        
        user = self.request.user
        message_type = self.request.query_params.get('message_type')
        order_id = self.request.query_params.get('order_id')
        conversation_id = self.request.query_params.get('conversation_id')
        
        # Base queryset with ordering (oldest first for chat continuity)
        queryset = Message.objects.select_related('user', 'order', 'conversation').prefetch_related('attachments').order_by('created_at')
        
        # Filter by conversation UUID if provided directly
        if conversation_id:
            queryset = queryset.filter(conversation_id=conversation_id)
            # Verify user has access to this conversation
            if not queryset.filter(conversation__user=user).exists():
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("You don't have access to this conversation.")
            return queryset
        
        # For order messages, get messages from the order's conversation
        if message_type == 'order' and order_id:
            from business.models import Order
            try:
                order = Order.objects.get(id=order_id)
                # Verify the user owns this order
                if order.client == user:
                    # Get the order's conversation (created by signal on order creation)
                    try:
                        conversation = Conversation.objects.get(order=order)
                        queryset = queryset.filter(conversation=conversation)
                    except Conversation.DoesNotExist:
                        # Create conversation if missing (backwards compatibility)
                        conversation = Conversation.create_for_order(order)
                        queryset = queryset.filter(conversation=conversation)
                else:
                    queryset = queryset.none()
            except Order.DoesNotExist:
                queryset = queryset.none()
        elif message_type == 'general':
            # For general messages, get or create the user's general conversation
            conversation, _ = Conversation.get_or_create_general(user)
            queryset = queryset.filter(conversation=conversation)
        else:
            # Fallback: show only user's own conversations
            queryset = queryset.filter(conversation__user=user)
            if message_type:
                queryset = queryset.filter(message_type=message_type)
        
        return queryset
    
    def get_serializer_class(self):
        """Use list serializer for list action"""
        if self.action == 'list':
            return MessageListSerializer
        return MessageSerializer
    
    def get_serializer_context(self):
        """Add request to serializer context for building absolute URLs"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def perform_create(self, serializer):
        """Handle file uploads and set sender, send email notification"""
        from .models import Conversation
        
        attachment_files = []
        if 'attachments' in self.request.FILES:
            attachment_files = self.request.FILES.getlist('attachments')
        
        # Set sender based on user role
        sender = 'user'
        is_support = hasattr(self.request.user, 'role') and self.request.user.role in ['admin', 'partner']
        if is_support:
            sender = 'support'
        
        # Determine the message owner (user field)
        message_owner = self.request.user
        order = serializer.validated_data.get('order')
        message_type = serializer.validated_data.get('message_type', 'general')
        
        # Get or create the appropriate Conversation
        conversation = None
        
        if message_type == 'order' and order:
            # For order messages: get the order's conversation (created by signal)
            try:
                conversation = Conversation.objects.get(order=order)
            except Conversation.DoesNotExist:
                # Create if missing (backwards compatibility)
                conversation = Conversation.create_for_order(order)
            
            if sender == 'user':
                # Client creating message for their own order
                if order.client != self.request.user:
                    from rest_framework.exceptions import PermissionDenied
                    raise PermissionDenied("You can only send messages for your own orders.")
                message_owner = self.request.user
            else:
                # Support creating message for client's order
                message_owner = order.client
        else:
            # For general messages: get or create user's general conversation
            conversation, _ = Conversation.get_or_create_general(message_owner)
        
        # Save the instance with conversation FK
        instance = serializer.save(
            user=message_owner,
            sender=sender,
            conversation=conversation,
            attachment_files=attachment_files
        )
        
        # Refresh from database to get all related fields
        instance.refresh_from_db()
        
        # Send email notification to admin for user messages, or to client for support messages
        if sender == 'user':
            send_new_message_notification(instance)
        # TODO: Add email notification to client when support sends a message
    
    @action(detail=False, methods=['post'], url_path='mark-read')
    def mark_read(self, request):
        """
        Mark messages and/or replies as read.
        Accepts:
        - notification_id: single notification ID (message or reply)
        - notification_ids: list of notification IDs
        - notification_type: 'message' or 'reply' (default: auto-detect)
        - message_type: filter by message type ('general', 'order')
        - order_id: filter by order
        """
        user = request.user
        notification_id = request.data.get('notification_id')
        notification_ids = request.data.get('notification_ids', [])
        notification_type = request.data.get('notification_type')  # 'message' or 'reply'
        message_type = request.data.get('message_type')
        order_id = request.data.get('order_id')
        
        messages_updated = 0
        replies_updated = 0
        
        # Handle single notification_id
        if notification_id:
            notification_ids = [notification_id]
        
        # If specific IDs provided, mark those
        if notification_ids:
            for nid in notification_ids:
                # Mark message as read (all messages including support replies are Message records)
                msg_count = Message.objects.filter(
                    id=nid,
                    conversation__user=user,
                    is_read=False
                ).update(is_read=True)
                messages_updated += msg_count
        else:
            # Bulk mark by filters
            queryset = Message.objects.filter(conversation__user=user, is_read=False)
            
            if message_type:
                queryset = queryset.filter(message_type=message_type)
            
            if order_id:
                queryset = queryset.filter(order_id=order_id)
            
            messages_updated = queryset.update(is_read=True)
        
        total_updated = messages_updated
        
        return Response({
            'success': True,
            'detail': f'{total_updated} notifications marked as read',
            'messages_updated': messages_updated,
            'total_updated': total_updated
        }, status=status.HTTP_200_OK)


# ==================== ANONYMOUS CHAT VIEWSET ====================
class AnonymousChatViewSet(viewsets.ViewSet):
    """
    ViewSet for anonymous user chat functionality
    No authentication required - uses session_id for identification
    Rate limited: 30 reads/minute, 10 writes/minute per session/IP
    No file attachments allowed for anonymous users
    """
    permission_classes = [permissions.AllowAny]
    
    def get_throttles(self):
        """Apply different throttle rates for read vs write operations"""
        if self.action == 'list':  # GET requests
            return [AnonChatReadThrottle()]
        elif self.action in ['create', 'mark_read']:  # POST requests
            return [AnonChatWriteThrottle()]
        return []
    
    def _get_client_ip(self, request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def _validate_session_id(self, session_id):
        """Validate session_id format (should be a UUID-like string)"""
        if not session_id:
            return False
        # Basic validation - should be 32-64 chars, alphanumeric with dashes
        import re
        return bool(re.match(r'^[a-zA-Z0-9\-]{32,64}$', session_id))
    
    def list(self, request):
        """
        Get messages for an anonymous conversation
        Requires session_id query parameter
        """
        session_id = request.query_params.get('session_id')
        
        if not session_id or not self._validate_session_id(session_id):
            return Response(
                {'error': 'Valid session_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            conversation = Conversation.objects.get(
                session_id=session_id,
                conversation_type='anonymous'
            )
            messages = Message.objects.filter(
                conversation=conversation
            ).order_by('created_at')
            
            serializer = AnonymousMessageSerializer(messages, many=True)
            return Response({
                'conversation_id': str(conversation.id),
                'messages': serializer.data,
                'status': conversation.status
            })
        except Conversation.DoesNotExist:
            # No conversation yet - return empty
            return Response({
                'conversation_id': None,
                'messages': [],
                'status': 'new'
            })
    
    def create(self, request):
        """
        Send a message in an anonymous chat
        Creates conversation if it doesn't exist
        Requires: session_id, content
        No file attachments allowed
        """
        session_id = request.data.get('session_id')
        content = request.data.get('content', '').strip()
        
        if not session_id or not self._validate_session_id(session_id):
            return Response(
                {'error': 'Valid session_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not content:
            return Response(
                {'error': 'Message content is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Limit message length for anonymous users
        if len(content) > 2000:
            return Response(
                {'error': 'Message too long (max 2000 characters)'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ip_address = self._get_client_ip(request)
        
        # Get or create conversation
        conversation, created = Conversation.get_or_create_anonymous(
            session_id=session_id,
            ip_address=ip_address
        )
        
        # Create the message
        message = Message.objects.create(
            conversation=conversation,
            message_type='anonymous',
            sender='anonymous',
            content=content,
            session_id=session_id,
            ip_address=ip_address,
            is_read=False
        )
        
        # Update conversation last_message_at
        conversation.last_message_at = message.created_at
        conversation.save(update_fields=['last_message_at', 'updated_at'])
        
        # Send notification to admin
        send_anonymous_message_notification(message, conversation)
        
        serializer = AnonymousMessageSerializer(message)
        return Response({
            'conversation_id': str(conversation.id),
            'message': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'], url_path='mark-read')
    def mark_read(self, request):
        """Mark messages as read for anonymous user"""
        session_id = request.data.get('session_id')
        
        if not session_id or not self._validate_session_id(session_id):
            return Response(
                {'error': 'Valid session_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            conversation = Conversation.objects.get(
                session_id=session_id,
                conversation_type='anonymous'
            )
            # Mark support messages as read
            count = Message.objects.filter(
                conversation=conversation,
                sender='support',
                is_read=False
            ).update(is_read=True)
            
            return Response({
                'success': True,
                'messages_updated': count
            })
        except Conversation.DoesNotExist:
            return Response({'success': True, 'messages_updated': 0})


def send_anonymous_message_notification(message, conversation):
    """Send email notification to admin when anonymous user sends a message"""
    try:
        admin_email = 'lewis_m@wordknox.com'
        subject = f'[Wordknox] New Anonymous Chat Message'
        body = f"""
New anonymous message received:

Session ID: {conversation.session_id[:16]}...
IP Address: {message.ip_address or 'Unknown'}
Time: {message.created_at.strftime('%Y-%m-%d %H:%M:%S')}

Message:
{message.content}

---
Reply to this message via the admin panel.
"""
        # Instantiate BaseEmail and send
        email = BaseEmail(
            subject=subject,
            message=body,
            recipient=admin_email
        )
        email.send()
    except Exception as e:
        # Log error but don't fail the request
        print(f"Failed to send anonymous message notification: {e}")


# ==================== ADMIN NOTIFICATION SUMMARY ====================
class AdminNotificationSummaryView(APIView):
    """
    API endpoint for admin notification dropdown
    Returns unreplied/unread counts and recent messages
    """
    permission_classes = [IsDeveloperOrAdmin]
    
    def get(self, request):
        # Contact Messages - unreplied
        contact_unreplied = ContactMessage.objects.filter(replied=False).count()
        contact_unread = ContactMessage.objects.filter(is_read=False).count()
        
        # General Messages - no admin reply
        general_unreplied = GeneralMessage.objects.filter(
            Q(admin_reply='') | Q(admin_reply__isnull=True)
        ).count()
        general_unread = GeneralMessage.objects.filter(status='new').count()
        
        # User Messages - messages from users without any support reply
        # A message needs reply if sender='user' and no support reply exists in same conversation
        user_messages_unreplied = Message.objects.filter(
            sender='user'
        ).annotate(
            has_support_reply=Exists(
                Message.objects.filter(
                    conversation=OuterRef('conversation'),
                    sender='support'
                )
            )
        ).filter(has_support_reply=False).count()
        
        total_unreplied = contact_unreplied + general_unreplied + user_messages_unreplied
        
        # Recent unreplied messages (last 10)
        recent_messages = []
        
        # Recent contact messages
        recent_contacts = ContactMessage.objects.filter(replied=False).order_by('-date_created')[:5]
        for msg in recent_contacts:
            recent_messages.append({
                'id': str(msg.id),
                'type': 'contact',
                'name': msg.name,
                'subject': msg.subject,
                'message': msg.message[:100] + '...' if len(msg.message) > 100 else msg.message,
                'sender_name': msg.name,
                'sender_email': msg.email,
                'created_at': msg.date_created.isoformat(),
                'priority': msg.priority,
                'is_read': msg.is_read,
                'message_type': 'contact',
            })
        
        # Recent general messages
        recent_general = GeneralMessage.objects.filter(
            Q(admin_reply='') | Q(admin_reply__isnull=True)
        ).order_by('-created_at')[:5]
        for msg in recent_general:
            recent_messages.append({
                'id': str(msg.id),
                'type': 'general',
                'name': msg.sender_name,
                'subject': msg.get_subject_display(),
                'message': msg.message[:100] + '...' if len(msg.message) > 100 else msg.message,
                'sender_name': msg.sender_name,
                'sender_email': msg.email,
                'created_at': msg.created_at.isoformat(),
                'priority': 'medium',
                'is_read': msg.status != 'new',
                'message_type': 'general',
            })
        
        # Recent user messages needing reply
        recent_user_msgs = Message.objects.filter(
            sender='user'
        ).annotate(
            has_support_reply=Exists(
                Message.objects.filter(
                    conversation=OuterRef('conversation'),
                    sender='support'
                )
            )
        ).filter(has_support_reply=False).select_related('user', 'order').order_by('-created_at')[:5]
        
        for msg in recent_user_msgs:
            user_name = msg.user.full_name if msg.user and msg.user.full_name else (msg.user.email if msg.user else 'User')
            recent_messages.append({
                'id': str(msg.id),
                'type': 'user_message',
                'title': f'{msg.get_message_type_display()} Message',
                'subject': f'{msg.get_message_type_display()} Message',
                'preview': msg.content[:100] + '...' if len(msg.content) > 100 else msg.content,
                'sender_name': user_name,
                'sender_email': msg.user.email if msg.user else '',
                'created_at': msg.created_at.isoformat(),
                'priority': 'medium',
                'is_read': msg.is_read,
                'order_id': str(msg.order.id) if msg.order else None,
                'message_type': msg.message_type,
            })
        
        # Sort by created_at descending
        recent_messages.sort(key=lambda x: x['created_at'], reverse=True)
        recent_messages = recent_messages[:10]
        
        return Response({
            'summary': {
                'contact_messages': {
                    'unreplied': contact_unreplied,
                    'unread': contact_unread,
                },
                'general_messages': {
                    'unreplied': general_unreplied,
                    'unread': general_unread,
                },
                'user_messages': {
                    'unreplied': user_messages_unreplied,
                },
                'total_unreplied': total_unreplied,
            },
            'recent_messages': recent_messages,
        })


def send_new_message_notification(message_instance):
    """Send email notification to admin when a new message is received"""
    try:
        admin_email = 'lewis_m@wordknox.com'
        
        if isinstance(message_instance, ContactMessage):
            subject = f'[Wordknox] New Contact Message from {message_instance.name}'
            body = f"""
New contact message received:

From: {message_instance.name} ({message_instance.email})
Phone: {message_instance.phone or 'Not provided'}
Subject: {message_instance.subject}
Priority: {message_instance.priority}
Source: {message_instance.source}

Message:
{message_instance.message}

---
View in admin: /admin/notifications/contactmessage/{message_instance.id}/change/
            """
        elif isinstance(message_instance, GeneralMessage):
            subject = f'[Wordknox] New General Inquiry from {message_instance.sender_name}'
            body = f"""
New general inquiry received:

From: {message_instance.sender_name} ({message_instance.email})
Phone: {message_instance.phone or 'Not provided'}
Subject: {message_instance.get_subject_display()}

Message:
{message_instance.message}

---
View in admin: /admin/notifications/generalmessage/{message_instance.id}/change/
            """
        elif isinstance(message_instance, Message):
            user_email = message_instance.user.email if message_instance.user else 'Unknown'
            subject = f'[Wordknox] New {message_instance.get_message_type_display()} Message from {user_email}'
            body = f"""
New in-system message received:

From: {user_email}
Type: {message_instance.get_message_type_display()}
Order: {message_instance.order.id if message_instance.order else 'None'}

Message:
{message_instance.content}

---
View in admin: /admin/notifications/message/{message_instance.id}/change/
            """
        else:
            return
        
        email = BaseEmail(
            subject=subject,
            message=body,
            recipient=admin_email
        )
        email.send()
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to send new message notification: {e}")


# ==================== CLIENT NOTIFICATION SUMMARY ====================
class ClientNotificationSummaryView(APIView):
    """
    Get notification summary for authenticated client users.
    Returns unread message counts and recent messages/replies
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Count unread support messages in user's conversations
        # Support messages are Message records with sender='support' in user's conversations
        unread_support_messages = Message.objects.filter(
            conversation__user=user,
            sender='support',
            is_read=False
        ).count()
        
        # Count unread order messages (from support)
        unread_order_messages = Message.objects.filter(
            conversation__user=user,
            message_type='order',
            sender='support',
            is_read=False
        ).count()
        
        # Count unread general messages (from support)
        unread_general_messages = Message.objects.filter(
            conversation__user=user,
            message_type='general',
            sender='support',
            is_read=False
        ).count()
        
        total_unread = unread_support_messages
        
        # Recent notifications (support messages in user's conversations)
        recent_notifications = []
        
        # Recent support messages in user's conversations
        recent_support_messages = Message.objects.filter(
            conversation__user=user,
            sender='support'
        ).select_related('order', 'conversation').order_by('-created_at')[:10]
        
        for msg in recent_support_messages:
            recent_notifications.append({
                'id': str(msg.id),
                'type': 'message',
                'title': f'{msg.get_message_type_display()} message from Support',
                'preview': msg.content[:100] + '...' if len(msg.content) > 100 else msg.content,
                'created_at': msg.created_at.isoformat(),
                'is_read': msg.is_read,
                'message_id': str(msg.id),
                'message_type': msg.message_type,
                'order_id': str(msg.order.id) if msg.order else None,
                'conversation_id': str(msg.conversation.id) if msg.conversation else None,
            })
        
        # Sort by created_at descending and limit
        recent_notifications.sort(key=lambda x: x['created_at'], reverse=True)
        recent_notifications = recent_notifications[:10]
        
        return Response({
            'summary': {
                'unread_support_messages': unread_support_messages,
                'unread_order_messages': unread_order_messages,
                'unread_general_messages': unread_general_messages,
                'total_unread': total_unread,
            },
            'recent_notifications': recent_notifications,
        })
