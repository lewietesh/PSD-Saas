# business/serializers.py
from rest_framework import serializers
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.db import models
from decimal import Decimal
import re
# ServiceRequest serializer for file upload and validation
from .models import ServiceRequest
from .models import Order, Testimonial, ContactMessage, Payment, Notification, PayPalPayment
from .utils import (
    generate_order_number, calculate_order_total, 
    validate_payment_method, send_order_confirmation_email
)

User = get_user_model()


class ServiceRequestSerializer(serializers.ModelSerializer):
    can_convert_to_order = serializers.SerializerMethodField()
    order_details = serializers.SerializerMethodField()
    service_name = serializers.CharField(source='service.name', read_only=True)
    pricing_tier_name = serializers.CharField(source='pricing_tier.name', read_only=True, allow_null=True)
    service_type = serializers.ChoiceField(
        choices=ServiceRequest.SERVICE_TYPE_CHOICES,
        default='technical'
    )
    pages = serializers.IntegerField(required=False, allow_null=True, min_value=1)
    
    def validate_email(self, value):
        if not value or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", value):
            raise serializers.ValidationError("Enter a valid email address.")
        return value

    def validate(self, attrs):
        errors = {}
        # Required fields
        if not attrs.get('email') or not attrs['email'].strip():
            errors['email'] = 'Email is required.'
        if not attrs.get('project_description') or not attrs['project_description'].strip():
            errors['project_description'] = 'Project description is required.'
        if not attrs.get('service'):
            errors['service'] = 'Service is required.'

        service_type = attrs.get('service_type', 'technical')
        # Writing-specific validation
        if service_type == 'writing':
            if not attrs.get('subject') or not attrs['subject'] or not str(attrs['subject']).strip():
                errors['subject'] = 'Subject is required for writing orders.'
            pages_value = attrs.get('pages')
            if not pages_value:
                errors['pages'] = 'Number of pages is required for writing orders.'
            elif pages_value < 1:
                errors['pages'] = 'Pages must be greater than zero.'
            if not attrs.get('formatting_style') or not str(attrs['formatting_style']).strip():
                errors['formatting_style'] = 'Formatting style is required for writing orders.'
            if not attrs.get('citations') or not str(attrs['citations']).strip():
                errors['citations'] = 'Citation instructions are required for writing orders.'

        if errors:
            raise serializers.ValidationError(errors)
        return attrs
    
    attachment = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = ServiceRequest
        fields = [
            'id', 'service', 'service_name', 'pricing_tier', 'pricing_tier_name',
            'name', 'email', 'project_description', 'budget',
            'timeline', 'service_type', 'subject', 'citations', 'formatting_style',
            'pages', 'attachment', 'status', 'order', 'created_at', 'updated_at',
            'can_convert_to_order', 'order_details'
        ]
        read_only_fields = ['id', 'status', 'order', 'created_at', 'updated_at', 'can_convert_to_order', 'order_details', 'service_name', 'pricing_tier_name']

    def get_can_convert_to_order(self, obj):
        """Check if this service request can be converted to an order"""
        return obj.order is None and obj.status != 'rejected'
    
    def get_order_details(self, obj):
        """Get order details if the service request has been converted"""
        if obj.order:
            return {
                'id': obj.order.id,
                'status': obj.order.status,
                'payment_status': obj.order.payment_status,
                'total_amount': obj.order.total_amount,
                'currency': obj.order.currency,
                'date_created': obj.order.date_created
            }
        return None

    def validate_attachment(self, value):
        if value:
            # Validate file size (max 15MB)
            if value.size > 15 * 1024 * 1024:
                raise serializers.ValidationError('Attachment file size must be under 15MB.')
            # Validate file type
            import os
            ext = os.path.splitext(value.name)[1].lower()
            allowed = ['.pdf', '.doc', '.docx', '.txt', '.jpg', '.jpeg', '.png', '.zip']
            if ext not in allowed:
                raise serializers.ValidationError('Invalid file type. Allowed: pdf, doc, docx, txt, jpg, jpeg, png, zip.')
            # Sanitize file name to prevent XSS (remove suspicious chars)
            import re
            safe_name = re.sub(r'[^\w.\-]', '_', value.name)
            value.name = safe_name
        return value

    def create(self, validated_data):
        # Save and trigger any post-create hooks (e.g., email notification)
        instance = super().create(validated_data)
        # Send auto-reply email to the service request sender
        try:
            from emails.base import send_service_request_autoreply
            send_service_request_autoreply(instance)
        except Exception as e:
            import logging
            logging.getLogger(__name__).exception('Failed to send service request auto-reply: %s', e)
        return instance

    def to_representation(self, instance):
        # Ensure validation errors are always returned in a clear, consistent format
        ret = super().to_representation(instance)
        return ret



class ContactMessageSerializer(serializers.ModelSerializer):
    """
    Serializer for contact form submissions with enhanced validation
    """
    
    class Meta:
        model = ContactMessage
        fields = [
            'id', 'name', 'email', 'phone', 'subject', 'message',
            'source', 'is_read', 'replied', 'priority', 'date_created'
        ]
        read_only_fields = ['id', 'is_read', 'replied', 'date_created']
    
    def validate_name(self, value):
        """Validate name field"""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long.")
        
        # Check for valid characters (letters, spaces, hyphens, apostrophes)
        if not re.match(r"^[a-zA-Z\s\-']+$", value.strip()):
            raise serializers.ValidationError("Name can only contain letters, spaces, hyphens, and apostrophes.")
        
        return value.strip().title()
    
    def validate_phone(self, value):
        """Validate phone number format"""
        if value:
            # Remove all non-digit characters
            cleaned_phone = re.sub(r'\D', '', value)
            
            # Check if it's a valid Kenyan number format
            if cleaned_phone.startswith('254'):
                if len(cleaned_phone) != 12:
                    raise serializers.ValidationError("Invalid Kenyan phone number format.")
            elif cleaned_phone.startswith('0'):
                if len(cleaned_phone) != 10:
                    raise serializers.ValidationError("Invalid phone number format.")
                # Convert to international format
                cleaned_phone = '254' + cleaned_phone[1:]
            else:
                if len(cleaned_phone) < 10 or len(cleaned_phone) > 15:
                    raise serializers.ValidationError("Invalid phone number format.")
            
            return '+' + cleaned_phone
        return value
    
    def validate_message(self, value):
        """Validate message content"""
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Message must be at least 10 characters long.")
        
        if len(value.strip()) > 2000:
            raise serializers.ValidationError("Message cannot exceed 2000 characters.")
        
        return value.strip()
    
    def validate_subject(self, value):
        """Validate subject field"""
        if value and len(value.strip()) > 255:
            raise serializers.ValidationError("Subject cannot exceed 255 characters.")
        return value.strip() if value else ""


class TestimonialCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating testimonials with validation
    """
    client_name = serializers.CharField(source='client.full_name', read_only=True)
    client_email = serializers.CharField(source='client.email', read_only=True)
    
    class Meta:
        model = Testimonial
        fields = [
            'id', 'client', 'client_name', 'client_email', 'project', 'service',
            'content', 'rating', 'featured', 'approved', 'date_created'
        ]
        read_only_fields = ['id', 'featured', 'approved', 'date_created']
    
    def validate_rating(self, value):
        """Validate rating is between 1-5"""
        if value is not None:
            if value < 1 or value > 5:
                raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
    
    def validate_content(self, value):
        """Validate testimonial content"""
        if len(value.strip()) < 20:
            raise serializers.ValidationError("Testimonial must be at least 20 characters long.")
        
        if len(value.strip()) > 1000:
            raise serializers.ValidationError("Testimonial cannot exceed 1000 characters.")
        
        return value.strip()
    
    def validate(self, attrs):
        """Cross-field validation"""
        project = attrs.get('project')
        service = attrs.get('service')
        
        # Must be related to either a project or service
        if not project and not service:
            raise serializers.ValidationError(
                "Testimonial must be associated with either a project or service."
            )
        
        return attrs


class TestimonialListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing testimonials with available client info
    """
    client_name = serializers.SerializerMethodField()
    profile_url = serializers.SerializerMethodField()
    verified = serializers.BooleanField(source='client.is_verified', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True, allow_null=True)
    
    class Meta:
        model = Testimonial
        fields = [
            'id', 'service_name', 'content', 'rating', 'featured',
            'date_created', 'client_name', 'profile_url', 'verified'
        ]
    
    def get_client_name(self, obj):
        """Get client's full name"""
        return obj.client.full_name if obj.client else 'Anonymous Client'
    
    def get_profile_url(self, obj):
        """Get client's profile image URL"""
        if obj.client.profile_img:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.client.profile_img.url)
            return obj.client.profile_img.url
        return None


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for payment records with validation
    """
    order_number = serializers.CharField(source='order.id', read_only=True)
    client_name = serializers.CharField(source='order.client.full_name', read_only=True)
    # Alias backend field date_created to created_at for frontend compatibility
    created_at = serializers.DateTimeField(source='date_created', read_only=True)
    # Frontend-friendly aliases
    reference = serializers.CharField(source='transaction_id', read_only=True)
    description = serializers.CharField(source='notes', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'order', 'order_number', 'client_name', 'amount', 'currency',
            'method', 'transaction_id', 'status', 'notes', 'date_created', 'created_at',
            'reference', 'description'
        ]
        read_only_fields = ['id', 'date_created']
    
    def validate_amount(self, value):
        """Validate payment amount"""
        if value <= 0:
            raise serializers.ValidationError("Payment amount must be greater than 0.")
        
        if value > Decimal('1000000.00'):  # 1 million limit
            raise serializers.ValidationError("Payment amount exceeds maximum limit.")
        
        return value
    
    def validate_method(self, value):
        """Validate payment method"""
        return validate_payment_method(value)
    
    def validate_transaction_id(self, value):
        """Validate transaction ID"""
        if not value or not value.strip():
            raise serializers.ValidationError("Transaction ID is required.")
        return value


class PayPalPaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for PayPal specific payment details
    """
    payment_id = serializers.CharField(source='payment.id', read_only=True)
    
    class Meta:
        model = PayPalPayment
        fields = [
            'payment', 'payment_id', 'paypal_order_id', 'paypal_payer_id',
            'paypal_payer_email', 'paypal_payment_id', 'paypal_status',
            'paypal_intent', 'paypal_create_time', 'paypal_update_time',
            'paypal_data', 'is_balance_deposit'
        ]
        read_only_fields = ['paypal_data']
        
    def validate_paypal_order_id(self, value):
        """Validate PayPal order ID format"""
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError("PayPal order ID is required and must be at least 3 characters.")
        
        return value.strip().upper()
    
    def validate(self, attrs):
        """Cross-field validation for payments"""
        order = attrs.get('order')
        amount = attrs.get('amount')
        
        if order and amount:
            # Check if payment amount doesn't exceed order total
            if amount > order.total_amount:
                raise serializers.ValidationError(
                    "Payment amount cannot exceed order total."
                )
            
            # Check for duplicate transaction IDs for the same order
            transaction_id = attrs.get('transaction_id')
            if transaction_id:
                existing_payment = Payment.objects.filter(
                    order=order,
                    transaction_id=transaction_id
                ).exclude(id=self.instance.id if self.instance else None).first()
                
                if existing_payment:
                    raise serializers.ValidationError(
                        "Transaction ID already exists for this order."
                    )
        
        return attrs


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating orders with comprehensive validation
    """
    order_number = serializers.CharField(read_only=True)
    client_name = serializers.CharField(source='client.full_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    pricing_tier_name = serializers.CharField(source='pricing_tier.name', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'client', 'client_name', 'service', 'service_name',
            'pricing_tier', 'pricing_tier_name', 'product', 'product_name',
            'total_amount', 'currency', 'status', 'payment_status',
            'payment_method', 'transaction_id', 'notes', 'due_date', 'date_created'
        ]
        read_only_fields = ['id', 'date_created']
    
    def validate_total_amount(self, value):
        """Validate order total amount"""
        if value <= 0:
            raise serializers.ValidationError("Order total must be greater than 0.")
        
        if value > Decimal('10000000.00'):  # 10 million limit
            raise serializers.ValidationError("Order total exceeds maximum limit.")
        
        return value
    
    def validate_due_date(self, value):
        """Validate due date is in the future"""
        if value and value <= timezone.now().date():
            raise serializers.ValidationError("Due date must be in the future.")
        return value
    
    def validate(self, attrs):
        """Cross-field validation for orders"""
        service = attrs.get('service')
        product = attrs.get('product')
        pricing_tier = attrs.get('pricing_tier')
        client = attrs.get('client')
        
        # Must have either service or product
        if not service and not product:
            raise serializers.ValidationError(
                "Order must be associated with either a service or product."
            )
        
        # Cannot have both service and product
        if service and product:
            raise serializers.ValidationError(
                "Order cannot be associated with both service and product."
            )
        
        # Validate pricing tier belongs to service
        if pricing_tier and service:
            if pricing_tier.service != service:
                raise serializers.ValidationError(
                    "Pricing tier does not belong to the selected service."
                )
        
        # Validate client role
        if client and client.role != 'client':
            raise serializers.ValidationError(
                "Orders can only be created for client users."
            )
        
        return attrs
    
    def create(self, validated_data):
        """Create order with automatic calculations"""
        # Calculate total if not provided
        if 'total_amount' not in validated_data:
            validated_data['total_amount'] = calculate_order_total(validated_data)
        
        order = super().create(validated_data)
        
        # Send confirmation email
        try:
            send_order_confirmation_email(order)
        except Exception as e:
            # Log error but don't fail order creation
            print(f"Failed to send order confirmation email: {e}")
        
        return order


class OrderListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing orders with essential information
    """
    client_name = serializers.CharField(source='client.full_name', read_only=True)
    client_email = serializers.CharField(source='client.email', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    pricing_tier_name = serializers.CharField(source='pricing_tier.name', read_only=True)
    payment_count = serializers.SerializerMethodField()
    total_paid = serializers.SerializerMethodField()
    attachment_count = serializers.SerializerMethodField()
    work_result_count = serializers.SerializerMethodField()
    message_thread = serializers.SerializerMethodField()
    unread_messages = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'id', 'client_name', 'client_email', 'service_name', 'product_name',
            'pricing_tier_name', 'total_amount', 'currency', 'status', 'payment_status',
            'payment_count', 'total_paid', 'attachment_count', 'work_result_count', 
            'message_thread', 'unread_messages', 'due_date', 'date_created'
        ]
    
    def get_payment_count(self, obj):
        """Get number of payments for this order"""
        return obj.payments.filter(status='paid').count()
    
    def get_total_paid(self, obj):
        """Get total amount paid for this order"""
        return obj.payments.filter(status='paid').aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0.00')
    
    def get_attachment_count(self, obj):
        """Get number of attachments"""
        return len(obj.attachments) if obj.attachments else 0
    
    def get_work_result_count(self, obj):
        """Get number of work results"""
        return len(obj.work_results) if obj.work_results else 0
    
    def get_message_thread(self, obj):
        """Get the order's message thread ID"""
        message = obj.messages.filter(message_type='order').first()
        return message.id if message else None
    
    def get_unread_messages(self, obj):
        """Count unread messages in order thread"""
        message = obj.messages.filter(message_type='order').first()
        if not message:
            return 0
        # TODO: Implement proper unread tracking with user FK on MessageReply
        # For now, return total reply count
        return message.message_replies.count()


class OrderDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for individual order view
    """
    client_details = serializers.SerializerMethodField()
    service_details = serializers.SerializerMethodField()
    product_details = serializers.SerializerMethodField()
    pricing_tier_details = serializers.SerializerMethodField()
    payments = PaymentSerializer(many=True, read_only=True)
    payment_summary = serializers.SerializerMethodField()
    file_attachments = serializers.SerializerMethodField()
    work_results = serializers.SerializerMethodField()
    message_thread = serializers.SerializerMethodField()
    unread_messages = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'id', 'client_details', 'service_details', 'product_details',
            'pricing_tier_details', 'total_amount', 'currency', 'status',
            'payment_status', 'payment_method', 'transaction_id', 'notes',
            'due_date', 'payments', 'payment_summary', 'file_attachments', 
            'work_results', 'message_thread', 'unread_messages',
            'date_created', 'date_updated'
        ]
    
    def get_client_details(self, obj):
        """Get client information"""
        if obj.client:
            return {
                'id': obj.client.id,
                'name': obj.client.full_name,
                'email': obj.client.email,
                'phone': obj.client.phone,
            }
        return None
    
    def get_service_details(self, obj):
        """Get service information"""
        if obj.service:
            return {
                'id': obj.service.id,
                'name': obj.service.name,
                'category': obj.service.service_category.name if obj.service.service_category else None,
                'pricing_model': obj.service.pricing_model,
            }
        return None
    
    def get_product_details(self, obj):
        """Get product information"""
        if obj.product:
            return {
                'id': obj.product.id,
                'name': obj.product.name,
                'category': obj.product.category,
                'price': obj.product.price,
            }
        return None
    
    def get_pricing_tier_details(self, obj):
        """Get pricing tier information"""
        if obj.pricing_tier:
            return {
                'id': obj.pricing_tier.id,
                'name': obj.pricing_tier.name,
                'price': obj.pricing_tier.price,
                'currency': obj.pricing_tier.currency,
            }
        return None
    
    def get_payment_summary(self, obj):
        """Get payment summary"""
        payments = obj.payments.all()
        total_paid = payments.filter(status='paid').aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0.00')
        
        return {
            'total_payments': payments.count(),
            'successful_payments': payments.filter(status='paid').count(),
            'failed_payments': payments.filter(status='failed').count(),
            'total_paid': total_paid,
            'balance_due': obj.total_amount - total_paid,
            'payment_status': 'fully_paid' if total_paid >= obj.total_amount else 'partial' if total_paid > 0 else 'unpaid'
        }
    
    def get_file_attachments(self, obj):
        """Get attachment file information"""
        if not obj.attachments:
            return []
        
        attachments = []
        for filename in obj.attachments:
            # Extract original filename (remove UUID prefix)
            display_name = filename.split('_', 1)[1] if '_' in filename else filename
            attachments.append({
                'filename': filename,
                'display_name': display_name,
                'url': f"/media/orders/attachments/{filename}",
                'type': 'attachment'
            })
        return attachments
    
    def get_work_results(self, obj):
        """Get work result file information"""
        if not obj.work_results:
            return []
        
        work_results = []
        for filename in obj.work_results:
            # Extract original filename (remove UUID prefix)
            display_name = filename.split('_', 1)[1] if '_' in filename else filename
            work_results.append({
                'filename': filename,
                'display_name': display_name,
                'url': f"/media/orders/work_results/{filename}",
                'type': 'work_result'
            })
        return work_results
    
    def get_message_thread(self, obj):
        """Get the order's message thread ID"""
        message = obj.messages.filter(message_type='order').first()
        return message.id if message else None
    
    def get_unread_messages(self, obj):
        """Count unread messages in order thread"""
        message = obj.messages.filter(message_type='order').first()
        if not message:
            return 0
        # TODO: Implement proper unread tracking with user FK on MessageReply
        # For now, return total reply count
        return message.message_replies.count()


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for system notifications
    """
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'user_name', 'type', 'title', 'subject', 'message',
            'is_read', 'priority', 'resource_id', 'resource_type', 'date_created'
        ]
        read_only_fields = ['id', 'date_created']
    
    def validate_title(self, value):
        """Validate notification title"""
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long.")
        return value.strip()
    
    def validate_message(self, value):
        """Validate notification message"""
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Message must be at least 5 characters long.")
        return value.strip()


# Bulk operation serializers
class BulkOrderStatusUpdateSerializer(serializers.Serializer):
    """
    Serializer for bulk order status updates
    """
    order_ids = serializers.ListField(
        child=serializers.CharField(),
        min_length=1,
        max_length=50
    )
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)
    notes = serializers.CharField(required=False, allow_blank=True)
    
    def validate_order_ids(self, value):
        """Validate that all order IDs exist"""
        existing_orders = Order.objects.filter(id__in=value).count()
        if existing_orders != len(value):
            raise serializers.ValidationError("Some order IDs do not exist.")
        return value


class OrderStatsSerializer(serializers.Serializer):
    """
    Serializer for order statistics
    """
    total_orders = serializers.IntegerField()
    pending_orders = serializers.IntegerField()
    completed_orders = serializers.IntegerField()
    cancelled_orders = serializers.IntegerField()


## AccountBalance serializer removed; balance handled under accounts app