# emails/base.py
import logging
import traceback


from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.utils import timezone

logger = logging.getLogger(__name__)


class BaseEmail:
    """Enhanced base email class with HTML template support"""
    
    def __init__(self, subject, message, recipient, from_email=None, template_name=None, context=None):
        self.subject = subject
        self.message = message
        self.recipient = recipient
        self.from_email = from_email or getattr(settings, 'DEFAULT_FROM_EMAIL', 'support@wordknox.com')
        self.template_name = template_name
        self.context = context or {}
        
        # Add default context for templates
        self.context.update({
            'company_name': getattr(settings, 'COMPANY_NAME', 'Wordknox'),
            'company_email': self.from_email,
            'company_phone': getattr(settings, 'COMPANY_PHONE', '+254 700 000 000'),
            'company_website': getattr(settings, 'COMPANY_WEBSITE', 'https://wordknox.com'),
            'support_email': getattr(settings, 'SUPPORT_EMAIL', 'support@wordknox.com'),
        })

    def send(self):
            """Enhanced send method with comprehensive error handling and logging"""
            logger.info(f"[EMAIL] Attempting to send email to {self.recipient}")
            logger.info(f"[EMAIL] Subject: {self.subject}")
            logger.info(f"[EMAIL] From: {self.from_email}")
            logger.info(f"[EMAIL] Template: {self.template_name if self.template_name else 'Plain text'}")
            
            # Log email configuration (without password)
            logger.info(f"[EMAIL CONFIG] Host: {getattr(settings, 'EMAIL_HOST', 'NOT SET')}")
            logger.info(f"[EMAIL CONFIG] Port: {getattr(settings, 'EMAIL_PORT', 'NOT SET')}")
            logger.info(f"[EMAIL CONFIG] Use TLS: {getattr(settings, 'EMAIL_USE_TLS', 'NOT SET')}")
            logger.info(f"[EMAIL CONFIG] Use SSL: {getattr(settings, 'EMAIL_USE_SSL', 'NOT SET')}")
            logger.info(f"[EMAIL CONFIG] Timeout: {getattr(settings, 'EMAIL_TIMEOUT', 'NOT SET')}")
            
            try:
                if self.template_name:
                    result = self._send_html_email()
                else:
                    result = self._send_simple_email()
                
                logger.info(f"[EMAIL SUCCESS] Email sent to {self.recipient}. Result: {result}")
                return result
                
            except Exception as e:
                logger.error(f"[EMAIL ERROR] Failed to send email to {self.recipient}")
                logger.error(f"[EMAIL ERROR] Error type: {type(e).__name__}")
                logger.error(f"[EMAIL ERROR] Error message: {str(e)}")
                logger.error(f"[EMAIL ERROR] Full traceback:\n{traceback.format_exc()}")
                
                # Try to provide more specific error information
                if "Connection refused" in str(e):
                    logger.error("[EMAIL ERROR] Connection refused - Check if EMAIL_HOST and EMAIL_PORT are correct")
                elif "Authentication failed" in str(e):
                    logger.error("[EMAIL ERROR] Authentication failed - Check EMAIL_HOST_USER and EMAIL_HOST_PASSWORD")
                elif "timed out" in str(e).lower():
                    logger.error("[EMAIL ERROR] Connection timed out - Check firewall settings and EMAIL_TIMEOUT")
                elif "certificate" in str(e).lower():
                    logger.error("[EMAIL ERROR] SSL/TLS certificate issue - Check EMAIL_USE_TLS and EMAIL_USE_SSL settings")
                
                raise  # Re-raise to let caller handle it
    
    def _send_html_email(self):
        """Send email with HTML template"""
        try:
            logger.info(f"[EMAIL] Rendering HTML template: {self.template_name}")
            html_content = render_to_string(self.template_name, self.context)
            text_content = strip_tags(html_content)
            
            logger.info(f"[EMAIL] Creating EmailMultiAlternatives message")
            msg = EmailMultiAlternatives(
                subject=self.subject,
                body=text_content,
                from_email=self.from_email,
                to=[self.recipient]
            )
            msg.attach_alternative(html_content, "text/html")
            
            logger.info(f"[EMAIL] Sending HTML email via SMTP")
            result = msg.send(fail_silently=False)
            logger.info(f"[EMAIL] HTML email sent successfully. Result: {result}")
            return result
            
        except Exception as e:
            logger.error(f"[EMAIL ERROR] Failed to send HTML email: {str(e)}")
            logger.error(f"[EMAIL ERROR] Traceback:\n{traceback.format_exc()}")
            logger.info(f"[EMAIL] Falling back to plain text email")
            return self._send_simple_email()
    
    def _send_simple_email(self):
        """Send plain text email"""
        try:
            logger.info(f"[EMAIL] Sending plain text email")
            result = send_mail(
                subject=self.subject,
                message=self.message,
                from_email=self.from_email,
                recipient_list=[self.recipient],
                fail_silently=False
            )
            logger.info(f"[EMAIL] Plain text email sent successfully. Result: {result}")
            return result
        except Exception as e:
            logger.error(f"[EMAIL ERROR] Failed to send plain text email: {str(e)}")
            logger.error(f"[EMAIL ERROR] Traceback:\n{traceback.format_exc()}")
            raise



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
            template_name='verify_email.html',
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
            template_name='password_recovery.html',
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


class NewMessageNotification(BaseEmail):
    """Notification email for new contact messages (notifications app)"""
    def __init__(self, message, admin_email):
        subject = f'New Contact Message from {message.sender_name} - {getattr(settings, "COMPANY_NAME", "Portfolio")}'
        
        # Truncate message content for email preview
        message_preview = message.message[:200] + '...' if len(message.message) > 200 else message.message
        
        simple_message = f'New contact message from {message.sender_name} ({message.email}): {message_preview}'
        
        context = {
            'sender_name': message.sender_name,
            'sender_email': message.email,
            'sender_phone': message.phone or 'Not provided',
            'message_subject': message.get_subject_display(),
            'message_content': message.message,
            'word_count': message.word_count,
            'message_id': str(message.id)[:8],
            'message_date': timezone.localtime(message.created_at).strftime('%B %d, %Y at %I:%M %p'),
            'ip_address': message.ip_address or 'Not captured',
            'device': message.device[:50] + '...' if message.device and len(message.device) > 50 else (message.device or 'Not captured'),
        }
        
        super().__init__(
            subject=subject,
            message=simple_message,
            recipient=admin_email,
            template_name='emails/new_message_notification.html',
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

