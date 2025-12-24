from django.core.management.base import BaseCommand
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging
import traceback

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Test email configuration and send a test email'

    def add_arguments(self, parser):
        parser.add_argument(
            '--to',
            type=str,
            dest='to',
            default='info@wordknox.com',
            help='Email address to send test email to'
        )
        parser.add_argument(
            '--html',
            action='store_true',
            dest='html',
            default=False,
            help='Send HTML email instead of plain text'
        )

    def handle(self, *args, **options):
        recipient = options.get('to', 'info@wordknox.com')
        use_html = options.get('html', False)
        
        self.stdout.write(self.style.WARNING('=' * 80))
        self.stdout.write(self.style.WARNING('Testing Email Configuration'))
        self.stdout.write(self.style.WARNING('=' * 80))
        
        # Display configuration
        self.stdout.write(self.style.HTTP_INFO('\n📧 Email Configuration:'))
        self.stdout.write(f"  EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
        self.stdout.write(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
        self.stdout.write(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
        self.stdout.write(f"  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
        self.stdout.write(f"  EMAIL_USE_SSL: {getattr(settings, 'EMAIL_USE_SSL', False)}")
        self.stdout.write(f"  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        self.stdout.write(f"  EMAIL_TIMEOUT: {getattr(settings, 'EMAIL_TIMEOUT', 'Not set')}")
        self.stdout.write(f"  DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
        self.stdout.write(f"  Recipient: {recipient}")
        self.stdout.write(f"  Format: {'HTML' if use_html else 'Plain Text'}")
        
        # Validate configuration
        self.stdout.write(self.style.HTTP_INFO('\n🔍 Validating Configuration:'))
        
        issues = []
        if settings.EMAIL_PORT == 465 and settings.EMAIL_USE_TLS:
            issues.append("⚠️  Port 465 should use SSL, not TLS")
            issues.append("    FIX: Set EMAIL_USE_SSL=True and EMAIL_USE_TLS=False")
        if settings.EMAIL_PORT == 587 and getattr(settings, 'EMAIL_USE_SSL', False):
            issues.append("⚠️  Port 587 should use TLS, not SSL")
            issues.append("    FIX: Set EMAIL_USE_TLS=True and EMAIL_USE_SSL=False")
        if not settings.EMAIL_HOST_PASSWORD:
            issues.append("⚠️  EMAIL_HOST_PASSWORD is not set")
        
        if issues:
            self.stdout.write(self.style.WARNING('\n  Configuration Issues Found:'))
            for issue in issues:
                self.stdout.write(f"    {issue}")
            self.stdout.write(self.style.WARNING('\n  Proceeding with test anyway...\n'))
        else:
            self.stdout.write(self.style.SUCCESS('  ✓ Configuration looks good\n'))
        
        # Test connection
        self.stdout.write(self.style.HTTP_INFO('📡 Testing SMTP Connection...'))
        try:
            from django.core.mail import get_connection
            connection = get_connection()
            connection.open()
            self.stdout.write(self.style.SUCCESS('  ✓ SMTP connection successful'))
            connection.close()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ✗ SMTP connection failed: {str(e)}'))
            self.stdout.write(self.style.ERROR(f'\n  Full error:\n{traceback.format_exc()}'))
            return
        
        # Send test email
        self.stdout.write(self.style.HTTP_INFO(f'\n📤 Sending test email to {recipient}...'))
        
        try:
            if use_html:
                # Test HTML email
                self.stdout.write('  Using HTML template...')
                html_content = f"""
                <html>
                    <body style="font-family: Arial, sans-serif; padding: 20px;">
                        <h2 style="color: #2c3e50;">Test Email from Django</h2>
                        <p>This is a <strong>test email</strong> to verify your email configuration.</p>
                        <div style="background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0;">
                            <h3>Configuration Details:</h3>
                            <ul>
                                <li><strong>Host:</strong> {settings.EMAIL_HOST}</li>
                                <li><strong>Port:</strong> {settings.EMAIL_PORT}</li>
                                <li><strong>TLS:</strong> {settings.EMAIL_USE_TLS}</li>
                                <li><strong>SSL:</strong> {getattr(settings, 'EMAIL_USE_SSL', False)}</li>
                            </ul>
                        </div>
                        <p style="color: #27ae60;"><strong>✓ If you received this email, your configuration is working!</strong></p>
                        <hr style="margin: 20px 0;">
                        <p style="color: #7f8c8d; font-size: 12px;">
                            Sent from Wordknox<br>
                            https://wordknox.com
                        </p>
                    </body>
                </html>
                """
                text_content = strip_tags(html_content)
                
                msg = EmailMultiAlternatives(
                    subject='Test Email from Django - Email Configuration Test',
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[recipient]
                )
                msg.attach_alternative(html_content, "text/html")
                result = msg.send(fail_silently=False)
            else:
                # Test plain text email
                self.stdout.write('  Using plain text...')
                result = send_mail(
                    subject='Test Email from Django - Email Configuration Test',
                    message=f"""
This is a test email to verify your email configuration.

Configuration Details:
- Host: {settings.EMAIL_HOST}
- Port: {settings.EMAIL_PORT}
- TLS: {settings.EMAIL_USE_TLS}
- SSL: {getattr(settings, 'EMAIL_USE_SSL', False)}

✓ If you received this email, your configuration is working!

---
Sent from Wordknox
https://wordknox.com
                    """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient],
                    fail_silently=False,
                )
            
            self.stdout.write(self.style.SUCCESS(f'\n✅ SUCCESS! Test email sent successfully'))
            self.stdout.write(self.style.SUCCESS(f'   Result: {result}'))
            self.stdout.write(self.style.SUCCESS(f'   Check {recipient} for the test email\n'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n❌ FAILED to send test email'))
            self.stdout.write(self.style.ERROR(f'   Error type: {type(e).__name__}'))
            self.stdout.write(self.style.ERROR(f'   Error message: {str(e)}'))
            
            # Provide specific troubleshooting advice
            self.stdout.write(self.style.WARNING('\n🔧 Troubleshooting Tips:'))
            if "Connection refused" in str(e):
                self.stdout.write('   • Check if EMAIL_HOST and EMAIL_PORT are correct')
                self.stdout.write('   • Verify firewall allows outbound connections on the port')
            elif "Authentication failed" in str(e) or "authentication" in str(e).lower():
                self.stdout.write('   • Verify EMAIL_HOST_USER and EMAIL_HOST_PASSWORD are correct')
                self.stdout.write('   • Check if your email provider requires app-specific passwords')
            elif "timed out" in str(e).lower():
                self.stdout.write('   • Check firewall settings')
                self.stdout.write('   • Increase EMAIL_TIMEOUT value')
                self.stdout.write('   • Verify the server allows SMTP connections')
            elif "certificate" in str(e).lower() or "ssl" in str(e).lower():
                self.stdout.write('   • For port 465: use EMAIL_USE_SSL=True, EMAIL_USE_TLS=False')
                self.stdout.write('   • For port 587: use EMAIL_USE_TLS=True, EMAIL_USE_SSL=False')
            
            self.stdout.write(self.style.ERROR(f'\n   Full traceback:'))
            self.stdout.write(f'{traceback.format_exc()}')
        
        self.stdout.write(self.style.WARNING('\n' + '=' * 80))