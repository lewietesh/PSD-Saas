# notifications/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth import get_user_model

from .models import Message, MessageReply
from .serializers import (
    MessageSerializer,
    MessageDetailSerializer,
    PublicMessageSerializer,
    MessageReplySerializer,
    OrderMessageSerializer
)

User = get_user_model()


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Message model
    - Public can create (AllowAny)
    - Admin can list, retrieve, update, delete (IsAdminUser)
    """
    queryset = Message.objects.select_related('assigned_to', 'user_id').prefetch_related('message_replies').all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'subject', 'assigned_to']
    search_fields = ['sender_name', 'email', 'message']
    ordering_fields = ['created_at', 'updated_at', 'status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter messages by type if specified"""
        queryset = super().get_queryset()
        message_type = self.request.query_params.get('message_type')
        
        if message_type in ['contact', 'order']:
            queryset = queryset.filter(message_type=message_type)
        
        # For non-staff users, only show their own order messages
        if not self.request.user.is_staff and message_type == 'order':
            queryset = queryset.filter(order__client=self.request.user)
        
        return queryset
    
    def get_permissions(self):
        """Allow anyone to create, require admin for other actions"""
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        message_type = self.request.query_params.get('message_type')
        if message_type == 'order' or self.action == 'for_order':
            return OrderMessageSerializer
        elif self.action == 'create':
            return PublicMessageSerializer
        elif self.action == 'retrieve':
            return MessageDetailSerializer
        return MessageSerializer
    
    def perform_create(self, serializer):
        """
        Create message with IP address and device info from request
        Send email notifications to admins
        """
        # Extract IP address
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0].strip()
        else:
            ip_address = self.request.META.get('REMOTE_ADDR')
        
        # Extract device (User-Agent)
        device = self.request.META.get('HTTP_USER_AGENT', '')
        
        # Check if authenticated user exists
        user_id = None
        if self.request.user and self.request.user.is_authenticated:
            user_id = self.request.user
        
        # Save message
        message = serializer.save(
            ip_address=ip_address,
            device=device,
            user_id=user_id
        )
        
        # Send email notifications to admins
        try:
            from emails.base import send_new_message_notification
            send_new_message_notification(message)
        except Exception as e:
            # Log error but don't fail the request
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to send notification emails: {e}")
        
        return message
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def add_reply(self, request, pk=None):
        """Add a reply to a message"""
        message = self.get_object()
        
        serializer = MessageReplySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(message=message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAdminUser])
    def assign(self, request, pk=None):
        """Assign message to an admin user"""
        message = self.get_object()
        
        user_id = request.data.get('assigned_to')
        if not user_id:
            return Response(
                {'error': 'assigned_to field is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(id=user_id, is_staff=True)
            message.assigned_to = user
            message.save(update_fields=['assigned_to', 'updated_at'])
            
            serializer = self.get_serializer(message)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid user ID or user is not staff'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAdminUser])
    def update_status(self, request, pk=None):
        """Update message status"""
        message = self.get_object()
        
        new_status = request.data.get('status')
        if not new_status:
            return Response(
                {'error': 'status field is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        valid_statuses = [choice[0] for choice in Message.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return Response(
                {'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        message.status = new_status
        message.save(update_fields=['status', 'updated_at'])
        
        serializer = self.get_serializer(message)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def for_order(self, request):
        """Get the message thread for a specific order"""
        order_id = request.query_params.get('order_id')
        if not order_id:
            return Response(
                {'error': 'order_id parameter required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Ensure user owns the order or is admin
        from business.models import Order
        try:
            order = Order.objects.get(id=order_id)
            if order.client != request.user and not request.user.is_staff:
                return Response(
                    {'error': 'Permission denied'},
                    status=status.HTTP_403_FORBIDDEN
                )
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        message = Message.objects.filter(
            order_id=order_id,
            message_type='order'
        ).prefetch_related('message_replies').first()
        
        if not message:
            return Response(
                {'error': 'Message thread not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = OrderMessageSerializer(message, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_order_reply(self, request):
        """Add a reply to an order message thread"""
        message_id = request.data.get('message_id')
        reply_text = request.data.get('reply_message')
        
        if not message_id or not reply_text:
            return Response(
                {'error': 'message_id and reply_message are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            message = Message.objects.get(id=message_id, message_type='order')
            
            # Ensure user owns the order or is admin
            if message.order and message.order.client != request.user and not request.user.is_staff:
                return Response(
                    {'error': 'Permission denied'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            reply = MessageReply.objects.create(
                message=message,
                sender_name=request.user.full_name or request.user.email,
                sender_type='admin' if request.user.is_staff else 'client',
                reply_message=reply_text
            )
            
            serializer = MessageReplySerializer(reply)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Message.DoesNotExist:
            return Response(
                {'error': 'Message thread not found'},
                status=status.HTTP_404_NOT_FOUND
            )
