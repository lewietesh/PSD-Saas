# ServePort/business/views.py
# Django imports
from datetime import datetime, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.models import Q, Sum, Count
from django.http import HttpResponse
from django.utils import timezone

# Django REST Framework imports
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

# Third-party imports
from django_filters.rest_framework import DjangoFilterBackend

# Local imports
from accounts.permissions import IsDeveloperOrAdmin, IsOwnerOrReadOnly, IsClientOwner
from .models import ServiceRequest, Order, Testimonial, ContactMessage, Payment, Notification
from .serializers import (
    ServiceRequestSerializer, OrderCreateSerializer, OrderListSerializer, OrderDetailSerializer,
    TestimonialCreateSerializer, TestimonialListSerializer,
    ContactMessageSerializer, PaymentSerializer, NotificationSerializer,
    BulkOrderStatusUpdateSerializer, OrderStatsSerializer
)
from .utils import (
    generate_order_number, process_payment, create_notification,
    send_contact_notification_email, auto_prioritize_contact_message,
    check_duplicate_contact, get_order_stats, get_dashboard_metrics,
    export_orders_to_csv, validate_order_transition, send_status_update_notification,
    mark_notifications_as_read
)
from .filters import OrderFilter, ContactMessageFilter, TestimonialFilter

User = get_user_model()

class ServiceRequestViewSet(viewsets.ModelViewSet):
    """
    API endpoint for creating and managing service requests (with file upload support).
    Anyone can POST (create), authenticated users can view their own, staff/admin can see all.
    """
    queryset = ServiceRequest.objects.all().select_related('service', 'pricing_tier', 'order')
    serializer_class = ServiceRequestSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.AllowAny()]
        elif self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        user = self.request.user
        
        # Anonymous users can't list/retrieve
        if not user.is_authenticated:
            return ServiceRequest.objects.none()
        
        # Staff/admin can see all service requests
        if user.is_staff:
            return super().get_queryset()
        
        # Regular authenticated users can only see their own (by email)
        return ServiceRequest.objects.filter(email=user.email).select_related('service', 'pricing_tier', 'order')

    def perform_create(self, serializer):
        """Create a new service request instance."""
        instance = serializer.save()
        return instance

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def convert_to_order(self, request, pk=None):
        """Convert a service request to an order"""
        from .utils import convert_service_request_to_order
        
        service_request = self.get_object()
        
        order, client_created, error_message = convert_service_request_to_order(service_request)
        
        if error_message:
            return Response(
                {"error": error_message},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({
            "message": "Service request successfully converted to order",
            "order_id": order.id,
            "client_created": client_created,
            "total_amount": float(order.total_amount),
            "order_status": order.status,
            "payment_status": order.payment_status
        }, status=status.HTTP_201_CREATED)


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing orders with comprehensive business logic.
    Handles order creation, updates, payments, refunds, and file management.
    """
    queryset = Order.objects.all().select_related('client', 'service', 'product', 'pricing_tier')
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action == 'list':
            return OrderListSerializer
        elif self.action in ['retrieve', 'update', 'partial_update']:
            return OrderDetailSerializer
        return OrderCreateSerializer
    
    def get_permissions(self):
        """
        Set permissions based on action
        """
        if self.action in ['create', 'list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsDeveloperOrAdmin]
        else:
            permission_classes = [IsDeveloperOrAdmin]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Filter queryset based on user role
        """
        queryset = super().get_queryset()
        user = self.request.user
        
        if not user.is_authenticated:
            return queryset.none()
        
        # Clients can only see their own orders
        if user.role == 'client':
            return queryset.filter(client=user)
        
        # Developers and admins can see all orders
        return queryset
    
    def perform_create(self, serializer):
        """
        Custom order creation logic
        """
        # Auto-assign client if not provided (for client users)
        if self.request.user.role == 'client':
            serializer.save(client=self.request.user)
        else:
            serializer.save()
        
        # Create notification for admins
        order = serializer.instance
        admin_users = self.request.user.__class__.objects.filter(
            role__in=['admin', 'developer']
        )
        
        for admin in admin_users:
            create_notification(
                user=admin,
                notification_type='order',
                title='New Order Received',
                message=f'New order {order.id[:8]} from {order.client.full_name or order.client.email}',
                resource_id=str(order.id),
                resource_type='order',
                priority='medium'
            )
    
    def perform_update(self, serializer):
        """
        Custom order update logic with status transition validation
        """
        old_status = self.get_object().status
        new_status = serializer.validated_data.get('status', old_status)
        
        if old_status != new_status:
            is_valid, message = validate_order_transition(self.get_object(), new_status)
            if not is_valid:
                raise serializers.ValidationError({'status': message})
        
        serializer.save()
        
        # Send notification if status changed
        if old_status != new_status:
            send_status_update_notification(serializer.instance, old_status, new_status)
    
    @action(detail=True, methods=['post'], permission_classes=[IsDeveloperOrAdmin])
    def mark_paid(self, request, pk=None):
        """
        Mark order as paid and update status
        """
        order = self.get_object()
        
        # Validate payment data
        payment_data = request.data
        required_fields = ['amount', 'method', 'transaction_id']
        
        for field in required_fields:
            if field not in payment_data:
                return Response(
                    {'error': f'{field} is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Process payment
        payment = process_payment(order, payment_data)
        
        if payment:
            return Response({
                'detail': 'Payment processed successfully',
                'payment_id': payment.id,
                'order_status': order.status,
                'payment_status': order.payment_status
            })
        else:
            return Response(
                {'error': 'Failed to process payment'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'], permission_classes=[IsDeveloperOrAdmin])
    def refund(self, request, pk=None):
        """
        Process order refund
        """
        order = self.get_object()
        
        if order.payment_status != 'paid':
            return Response(
                {'error': 'Cannot refund unpaid order'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update order status
        old_status = order.status
        order.status = 'refunded'
        order.payment_status = 'refunded'
        order.save()
        
        # Create refund payment record
        Payment.objects.create(
            order=order,
            amount=-order.total_amount,  # Negative amount for refund
            currency=order.currency,
            method='refund',
            transaction_id=f"REFUND-{order.id[:8]}",
            status='paid',
            notes=request.data.get('notes', 'Order refunded')
        )
        
        # Send notification
        send_status_update_notification(order, old_status, 'refunded')
        
        return Response({'detail': 'Order refunded successfully'})
    
    @action(detail=False, methods=['post'], permission_classes=[IsDeveloperOrAdmin])
    def bulk_update_status(self, request):
        """
        Bulk update order statuses
        """
        serializer = BulkOrderStatusUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            order_ids = serializer.validated_data['order_ids']
            new_status = serializer.validated_data['status']
            notes = serializer.validated_data.get('notes', '')
            
            # Validate all orders exist and transitions are valid
            orders = Order.objects.filter(id__in=order_ids)
            
            if orders.count() != len(order_ids):
                return Response(
                    {'error': 'Some orders not found'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            invalid_transitions = []
            for order in orders:
                is_valid, message = validate_order_transition(order, new_status)
                if not is_valid:
                    invalid_transitions.append(f"Order {order.id[:8]}: {message}")
            
            if invalid_transitions:
                return Response(
                    {'error': 'Invalid transitions', 'details': invalid_transitions},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Update all orders
            updated_count = orders.update(status=new_status)
            
            # Add notes if provided
            if notes:
                for order in orders:
                    order.notes = f"{order.notes}\n{notes}" if order.notes else notes
                    order.save()
            
            return Response({
                'detail': f'Successfully updated {updated_count} orders',
                'updated_orders': list(orders.values_list('id', flat=True))
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[IsDeveloperOrAdmin])
    def statistics(self, request):
        """
        Get comprehensive order statistics
        """
        # Date filtering
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        
        if date_from:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
        if date_to:
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
        
        stats = get_order_stats(date_from, date_to)
        
        serializer = OrderStatsSerializer(stats)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsDeveloperOrAdmin])
    def export_csv(self, request):
        """
        Export orders to CSV
        """
        queryset = self.filter_queryset(self.get_queryset())
        csv_data, filename = export_orders_to_csv(queryset)
        
        response = HttpResponse(csv_data, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def timeline(self, request, pk=None):
        """
        Get order timeline/history
        """
        order = self.get_object()
        
        # Collect timeline events
        timeline = []
        
        # Order creation
        timeline.append({
            'date': order.date_created,
            'event': 'Order Created',
            'description': f'Order created for {order.client.full_name or order.client.email}',
            'type': 'order'
        })
        
        # Payment events
        for payment in order.payments.all():
            timeline.append({
                'date': payment.date_created,
                'event': f'Payment {payment.status.title()}',
                'description': f'{payment.currency} {payment.amount} via {payment.method}',
                'type': 'payment'
            })
        
        # Sort by date
        timeline.sort(key=lambda x: x['date'], reverse=True)
        
        return Response({'timeline': timeline})

    @action(detail=True, methods=['post'], permission_classes=[IsDeveloperOrAdmin])
    def upload_attachment(self, request, pk=None):
        """
        Upload an attachment file to the order
        """
        from .utils import upload_order_attachment
        
        order = self.get_object()
        
        if 'file' not in request.FILES:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        uploaded_file = request.FILES['file']
        filename, error_message = upload_order_attachment(order, uploaded_file)
        
        if error_message:
            return Response(
                {'error': error_message},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({
            'message': 'File uploaded successfully',
            'filename': filename,
            'url': f"/media/orders/attachments/{filename}"
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsDeveloperOrAdmin])
    def upload_work_result(self, request, pk=None):
        """
        Upload a work result file to the order
        """
        from .utils import upload_order_work_result
        
        order = self.get_object()
        
        if 'file' not in request.FILES:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        uploaded_file = request.FILES['file']
        filename, error_message = upload_order_work_result(order, uploaded_file)
        
        if error_message:
            return Response(
                {'error': error_message},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({
            'message': 'Work result uploaded successfully',
            'filename': filename,
            'url': f"/media/orders/work_results/{filename}"
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'], permission_classes=[IsDeveloperOrAdmin])
    def delete_file(self, request, pk=None):
        """
        Delete a file from the order
        """
        from .utils import delete_order_file
        
        order = self.get_object()
        filename = request.data.get('filename')
        file_type = request.data.get('file_type', 'attachment')  # 'attachment' or 'work_result'
        
        if not filename:
            return Response(
                {'error': 'Filename is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        success, error_message = delete_order_file(order, filename, file_type)
        
        if error_message:
            return Response(
                {'error': error_message},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({
            'message': f'File {filename} deleted successfully'
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], parser_classes=[MultiPartParser, FormParser])
    def upload_attachments(self, request, pk=None):
        """
        Upload client attachments to an order with strict validation:
        - Only PDF, Word (.doc, .docx), and .txt files
        - Max 5MB per file
        - Max 10 files per order
        """
        import os
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        
        order = self.get_object()
        
        # Check if user owns this order (clients can only upload to their own orders)
        if request.user.role == 'client' and order.client != request.user:
            return Response(
                {'error': 'You can only upload files to your own orders'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        files = request.FILES.getlist('files')
        
        if not files:
            return Response(
                {'error': 'No files provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check total file count limit
        current_count = len(order.attachments)
        if current_count + len(files) > 10:
            return Response(
                {'error': f'Maximum 10 files per order. You have {current_count} file(s) already.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Allowed file extensions and max size
        ALLOWED_EXTENSIONS = ['.pdf', '.doc', '.docx', '.txt']
        MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB in bytes
        
        uploaded_files = []
        errors = []
        
        for file in files:
            # Validate file extension
            file_ext = os.path.splitext(file.name)[1].lower()
            if file_ext not in ALLOWED_EXTENSIONS:
                errors.append(f'{file.name}: Invalid file type. Only PDF, Word, and TXT files allowed.')
                continue
            
            # Validate file size
            if file.size > MAX_FILE_SIZE:
                errors.append(f'{file.name}: File too large. Maximum 5MB per file.')
                continue
            
            # Generate safe filename
            safe_filename = f"{order.id}_{timezone.now().strftime('%Y%m%d_%H%M%S')}_{file.name}"
            file_path = f'orders/attachments/{safe_filename}'
            
            try:
                # Save file
                saved_path = default_storage.save(file_path, ContentFile(file.read()))
                
                # Add to order's attachments array
                order.add_attachment(safe_filename)
                uploaded_files.append({
                    'filename': safe_filename,
                    'original_name': file.name,
                    'size': file.size,
                    'url': default_storage.url(saved_path)
                })
            except Exception as e:
                errors.append(f'{file.name}: Upload failed - {str(e)}')
        
        response_data = {
            'message': f'{len(uploaded_files)} file(s) uploaded successfully',
            'uploaded_files': uploaded_files,
            'total_attachments': len(order.attachments)
        }
        
        if errors:
            response_data['errors'] = errors
        
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def timeline(self, request, pk=None):
        """
        Get minimal timeline of activities for an order.
        Returns key events like order creation, status changes, payments, messages, and file uploads.
        """
        from .models import OrderActivity
        
        order = self.get_object()
        
        # Check if user can access this order
        if request.user.role == 'client' and order.client != request.user:
            return Response(
                {'error': 'You can only view timeline for your own orders'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get all activities for this order
        activities = order.activities.all()
        
        timeline_data = []
        for activity in activities:
            timeline_data.append({
                'id': activity.id,
                'type': activity.activity_type,
                'description': activity.description,
                'created_by': activity.created_by.full_name if activity.created_by else 'System',
                'created_at': activity.created_at.isoformat()
            })
        
        return Response({
            'order_id': str(order.id),
            'timeline': timeline_data,
            'count': len(timeline_data)
        })


class ContactMessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing contact messages.
    Anyone can create messages, only admins can manage them.
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    filterset_class = ContactMessageFilter
    filter_backends = [DjangoFilterBackend]
    
    def get_permissions(self):
        """
        Allow anyone to create contact messages, restrict other actions
        """
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsDeveloperOrAdmin]
        
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        """
        Custom contact message creation with validation and notifications
        """
        # Check for duplicates
        email = serializer.validated_data['email']
        phone = serializer.validated_data.get('phone')
        
        if check_duplicate_contact(email, phone):
            # Still create but mark as potential duplicate
            contact = serializer.save()
            contact.notes = "Potential duplicate submission"
            contact.save()
        else:
            contact = serializer.save()
        
        # Auto-prioritize
        priority = auto_prioritize_contact_message(contact)
        contact.priority = priority
        contact.save()
        
        # Send notification email
        send_contact_notification_email(contact)
        
        # Create admin notification
        admin_users = User.objects.filter(role__in=['admin', 'developer'])


        
        for admin in admin_users:
            create_notification(
                user=admin,
                notification_type='contact',
                title='New Contact Message',
                message=f'New message from {contact.name} - {contact.subject}',
                resource_id=str(contact.id),
                resource_type='contact',
                priority=priority
            )
    
    @action(detail=True, methods=['post'], permission_classes=[IsDeveloperOrAdmin])
    def mark_read(self, request, pk=None):
        """
        Mark contact message as read
        """
        message = self.get_object()
        message.is_read = True
        message.save()
        
        return Response({'detail': 'Message marked as read'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsDeveloperOrAdmin])
    def mark_replied(self, request, pk=None):
        """
        Mark contact message as replied
        """
        message = self.get_object()
        message.replied = True
        message.is_read = True
        message.save()
        
        return Response({'detail': 'Message marked as replied'})
    
    @action(detail=False, methods=['get'], permission_classes=[IsDeveloperOrAdmin])
    def pending(self, request):
        """
        Get pending contact messages
        """
        pending_messages = self.get_queryset().filter(
            is_read=False,
            replied=False
        ).order_by('-priority', '-date_created')
        
        serializer = self.get_serializer(pending_messages, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsDeveloperOrAdmin])
    def bulk_mark_read(self, request):
        """
        Bulk mark messages as read
        """
        message_ids = request.data.get('message_ids', [])
        
        if not message_ids:
            return Response(
                {'error': 'message_ids required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        updated_count = self.get_queryset().filter(
            id__in=message_ids
        ).update(is_read=True)
        
        return Response({
            'detail': f'Marked {updated_count} messages as read'
        })


class TestimonialViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing testimonials with approval workflow
    """
    queryset = Testimonial.objects.all().select_related('client', 'project', 'service')
    filterset_class = TestimonialFilter
    filter_backends = [DjangoFilterBackend]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TestimonialCreateSerializer
        return TestimonialListSerializer
    
    def get_permissions(self):
        """
        Clients can create testimonials, admins manage them
        """
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]  # Public testimonials
        else:
            permission_classes = [IsDeveloperOrAdmin]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Filter testimonials based on user and approval status
        """
        queryset = super().get_queryset()
        user = self.request.user
        
        # Public views only see approved testimonials
        if not user.is_authenticated or user.role not in ['admin', 'developer']:
            return queryset.filter(approved=True)
        
        # Clients see their own testimonials
        if user.role == 'client':
            return queryset.filter(client=user)
        
        # Admins see all
        return queryset
    
    def perform_create(self, serializer):
        """
        Auto-assign client for testimonial creation
        """
        if self.request.user.role == 'client':
            serializer.save(client=self.request.user)
        else:
            serializer.save()
        
        # Notify admins of new testimonial
        testimonial = serializer.instance
        admin_users = self.request.user.__class__.objects.filter(
            role__in=['admin', 'developer']
        )
        
        for admin in admin_users:
            create_notification(
                user=admin,
                notification_type='review',
                title='New Testimonial Submitted',
                message=f'New testimonial from {testimonial.client.full_name or testimonial.client.email}',
                resource_id=str(testimonial.id),
                resource_type='testimonial',
                priority='low'
            )
    
    @action(detail=True, methods=['post'], permission_classes=[IsDeveloperOrAdmin])
    def approve(self, request, pk=None):
        """
        Approve testimonial
        """
        testimonial = self.get_object()
        testimonial.approved = True
        testimonial.save()
        
        return Response({'detail': 'Testimonial approved'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsDeveloperOrAdmin])
    def feature(self, request, pk=None):
        """
        Feature/unfeature testimonial
        """
        testimonial = self.get_object()
        testimonial.featured = not testimonial.featured
        testimonial.save()
        
        action = 'featured' if testimonial.featured else 'unfeatured'
        return Response({'detail': f'Testimonial {action}'})
    
#     @action(detail=False, methods=['get'])
#     def featured(self, request):

class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user notifications.
    Users can only access their own notifications.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    filter_backends = [DjangoFilterBackend]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsDeveloperOrAdmin()]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_authenticated:
            return queryset.none()
        return queryset.filter(user=user)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def mark_read(self, request):
        ids = request.data.get('notification_ids')
        updated_count = mark_notifications_as_read(request.user, ids)
        return Response({'detail': f'Marked {updated_count} notifications as read'})

class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing payments.
    Clients can only access payments for their own orders.
    """
    queryset = Payment.objects.select_related('order', 'order__client').all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    pagination_class = None  # Return unpaginated list for frontend compatibility

    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsDeveloperOrAdmin()]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_authenticated:
            return queryset.none()
        # Return payments directly made by the user OR linked to orders owned by the user
        if user.role == 'client':
            return queryset.filter(
                (Q(user=user)) | (Q(order__client=user))
            )
        # Developers/Admins get all by default via permission control
        return queryset
        
