# emails/base.py
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging
from django.utils import timezone
logger = logging.getLogger(__name__)


class BaseEmail:
    """Enhanced base email class with HTML template support"""
    
    def __init__(self, subject, message, recipient, from_email=None, template_name=None, context=None):
        self.subject = subject
        self.message = message
        self.recipient = recipient
        self.from_email = from_email or getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@portfolio.com')
        self.template_name = template_name
        self.context = context or {}
        
        # Add default context for templates
        self.context.update({
            'company_name': getattr(settings, 'COMPANY_NAME', 'Portfolio'),
            'company_email': self.from_email,
            'company_phone': getattr(settings, 'COMPANY_PHONE', '+254 700 000 000'),
            'company_website': getattr(settings, 'COMPANY_WEBSITE', 'https://portfolio.com'),
            'support_email': getattr(settings, 'SUPPORT_EMAIL', 'support@portfolio.com'),
        })

    def send(self):
        """Enhanced send method with HTML template support"""
        if self.template_name:
            return self._send_html_email()
        else:
            # Fallback to original simple send
            return self._send_simple_email()
    
    def _send_html_email(self):
        """Send email with HTML template"""
        try:
            html_content = render_to_string(self.template_name, self.context)
            text_content = strip_tags(html_content)
            
            msg = EmailMultiAlternatives(
                subject=self.subject,
                body=text_content,
                from_email=self.from_email,
                to=[self.recipient]
            )
            msg.attach_alternative(html_content, "text/html")
            
            result = msg.send()
            logger.info(f"HTML email sent to {self.recipient}: {self.subject}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to send HTML email to {self.recipient}: {e}")
            # Fallback to simple email
            return self._send_simple_email()
    
    def _send_simple_email(self):
        """Original simple send method"""
        return send_mail(
            self.subject,
            self.message,
            self.from_email,
            [self.recipient],
            fail_silently=False
        )



# Keep your existing classes but enhance them
class VerifyEmail(BaseEmail):
    def __init__(self, recipient, code):
        subject = 'Verify Your Email - Portfolio API'
        message = f'Your email verification code is: {code}. This code expires in 10 minutes.'
        
        # Enhanced with template support
        context = {
            'verification_code': code,
            'user_name': recipient.split('@')[0],
            'expiry_minutes': 10,
        }
        
        super().__init__(
            subject=subject,
            message=message,
            recipient=recipient,
            template_name='emails/verify_email.html',
            context=context
        )


class RecoverPasswordEmail(BaseEmail):
    def __init__(self, recipient, code):
        subject = 'Password Reset Code - Portfolio API'
        message = f'Your password reset code is: {code}. This code expires in 10 minutes.'
        
        # Enhanced with template support
        context = {
            'reset_code': code,
            'user_name': recipient.split('@')[0],
            'expiry_minutes': 10,
        }
        
        super().__init__(
            subject=subject,
            message=message,
            recipient=recipient,
            template_name='emails/password_recovery.html',
            context=context
        )


# New email types for your additional needs
class ServiceRequestAutoReply(BaseEmail):
    def __init__(self, service_request):
        subject = f'Thank you for your service request! - {getattr(settings, "COMPANY_NAME", "Portfolio")}'
        message = f'Thank you {service_request.name or "there"} for your service request. We will get back to you within 24 hours.'
        
        context = {
            'client_name': service_request.name or 'there',
            'service_name': service_request.service.name,
            'project_description': service_request.project_description,
            'budget': service_request.budget,
            'timeline': service_request.timeline,
            'pricing_tier': service_request.pricing_tier.name if service_request.pricing_tier else None,
            'request_id': str(service_request.id)[:8],
            'submitted_date': timezone.localtime(service_request.created_at).strftime('%B %d, %Y at %I:%M %p'),
            'response_time': '24 hours',
        }
        
        super().__init__(
            subject=subject,
            message=message,
            recipient=service_request.email,
            template_name='emails/service_request_autoreply.html',
            context=context
        )


class OrderConfirmationEmail(BaseEmail):
    def __init__(self, order):
        subject = f'Order Confirmation #{str(order.id)[:8]} - {getattr(settings, "COMPANY_NAME", "Portfolio")}'
        message = f'Your order has been confirmed. Order ID: {str(order.id)[:8]}'
        
        context = {
            'client_name': order.client.first_name or order.client.email.split('@')[0],
            'order_number': str(order.id)[:8],
            'service_name': order.service.name if order.service else 'Custom Service',
            'product_name': order.product.name if order.product else None,
            'total_amount': order.total_amount,
            'currency': order.currency,
            'order_status': order.get_status_display(),
            'payment_status': order.get_payment_status_display(),
            'order_date': timezone.localtime(order.date_created).strftime('%B %d, %Y at %I:%M %p'),
        }
        
        super().__init__(
            subject=subject,
            message=message,
            recipient=order.client.email,
            template_name='emails/order_confirmation.html',
            context=context
        )


class ContactMessageNotification(BaseEmail):
    def __init__(self, contact_message, admin_email):
        subject = f'New Contact Message from {contact_message.name} - {getattr(settings, "COMPANY_NAME", "Portfolio")}'
        message = f'New contact message from {contact_message.name} ({contact_message.email}): {contact_message.message}'
        
        context = {
            'sender_name': contact_message.name,
            'sender_email': contact_message.email,
            'sender_phone': contact_message.phone,
            'message_subject': contact_message.subject,
            'message_content': contact_message.message,
            'message_source': contact_message.get_source_display(),
            'priority': contact_message.get_priority_display(),
            'message_date': timezone.localtime(contact_message.date_created).strftime('%B %d, %Y at %I:%M %p'),
        }
        
        super().__init__(
            subject=subject,
            message=message,
            recipient=admin_email,
            template_name='emails/contact_notification.html',
            context=context
        )


# Utility functions for easy usage
def send_service_request_autoreply(service_request):
    """Send auto-reply for service request"""
    email = ServiceRequestAutoReply(service_request)
    return email.send()

def send_order_confirmation(order):
    """Send order confirmation email"""
    email = OrderConfirmationEmail(order)
    return email.send()

def send_contact_notification(contact_message, admin_email=None):
    """Send contact notification to admin"""
    admin_email = admin_email or getattr(settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL)
    email = ContactMessageNotification(contact_message, admin_email)
    return email.send()