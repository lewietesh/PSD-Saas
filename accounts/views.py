"""
Accounts app views for user authentication, registration, and profile management.
"""

# Python standard library
import random
import string
import time
import logging
import traceback

# Django core
from django.contrib.auth import authenticate, login, logout as django_logout
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Django REST Framework
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

# Third-party
from social_django.utils import load_strategy, load_backend
from social_core.backends.google import GoogleOAuth2
import requests

# Local imports
from .models import User, ClientProfile, Partner
from .serializers import (
    UserBasicSerializer,
    UserDetailSerializer,
    UserRegistrationSerializer,
    UserUpdateSerializer,
    ClientProfileSerializer,
    ClientProfileUpdateSerializer,
    PartnerPublicSerializer,
    PasswordChangeSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    EmailVerificationSerializer,
    EmailVerificationConfirmSerializer,
    ChangePasswordSerializer,
    Toggle2FASerializer,
)
from .permissions import IsDeveloperOrAdmin, IsOwnerOrReadOnly

# Decimal for currency handling
from decimal import Decimal

# Initialize logger
logger = logging.getLogger(__name__)


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def generate_verification_code():
    """Generate a 6-digit verification code."""
    return ''.join(random.choices(string.digits, k=6))


def send_verification_email(email, code, purpose):
    """
    Send verification code via email with comprehensive error handling.
    
    Args:
        email: Recipient email address
        code: Verification code
        purpose: 'email_verification' or 'password_reset'
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    timestamp = int(time.time())
    
    # TESTING: Print verification code to console
    print(f"\n{'='*60}")
    print(f"🔐 VERIFICATION CODE FOR TESTING")
    print(f"{'='*60}")
    print(f"Email: {email}")
    print(f"Code: {code}")
    print(f"Purpose: {purpose}")
    print(f"{'='*60}\n")
    
    logger.info(f"[EMAIL {timestamp}] Starting email send for {email}")
    logger.info(f"[EMAIL {timestamp}] Purpose: {purpose}, Code: {code}")
    logger.info(f"[EMAIL {timestamp}] FROM: {getattr(settings, 'DEFAULT_FROM_EMAIL', 'NOT SET')}")
    logger.info(f"[EMAIL {timestamp}] Backend: {getattr(settings, 'EMAIL_BACKEND', 'NOT SET')}")
    
    try:
        # Try using custom email classes first
        if purpose == 'email_verification':
            try:
                from emails.base import VerifyEmail
                logger.info(f"[EMAIL {timestamp}] Using VerifyEmail class")
                email_obj = VerifyEmail(email, code)
                result = email_obj.send()
                logger.info(f"[EMAIL {timestamp}] VerifyEmail result: {result}")
                return bool(result)
            except ImportError as e:
                logger.warning(f"[EMAIL {timestamp}] VerifyEmail import failed: {e}")
            except Exception as e:
                logger.error(f"[EMAIL {timestamp}] VerifyEmail error: {e}")
                logger.error(f"[EMAIL {timestamp}] Traceback: {traceback.format_exc()}")
                
        elif purpose == 'password_reset':
            try:
                from emails.base import RecoverPasswordEmail
                logger.info(f"[EMAIL {timestamp}] Using RecoverPasswordEmail class")
                email_obj = RecoverPasswordEmail(email, code)
                result = email_obj.send()
                logger.info(f"[EMAIL {timestamp}] RecoverPasswordEmail result: {result}")
                return bool(result)
            except ImportError as e:
                logger.warning(f"[EMAIL {timestamp}] RecoverPasswordEmail import failed: {e}")
            except Exception as e:
                logger.error(f"[EMAIL {timestamp}] RecoverPasswordEmail error: {e}")
        
        # Fallback to plain text email
        logger.info(f"[EMAIL {timestamp}] Using fallback plain text email")
        
        subject_map = {
            'email_verification': 'Email Verification Code - Wordknox',
            'password_reset': 'Password Reset Code - Wordknox'
        }
        
        message_map = {
            'email_verification': f"""Hello,

Your email verification code is: {code}

This code will expire in 10 minutes.

If you didn't request this code, please ignore this email.

Best regards,
Wordknox Team
""",
            'password_reset': f"""Hello,

Your password reset code is: {code}

This code will expire in 10 minutes.

If you didn't request this password reset, please ignore this email and your password will remain unchanged.

Best regards,
Wordknox Team
"""
        }
        
        subject = subject_map.get(purpose, 'Verification Code')
        message = message_map.get(purpose, f'Your verification code is: {code}')
        
        logger.info(f"[EMAIL {timestamp}] Subject: {subject}")
        logger.info(f"[EMAIL {timestamp}] To: {email}")
        
        sent = send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False
        )
        
        logger.info(f"[EMAIL {timestamp}] send_mail result: {sent}")
        return bool(sent)
        
    except Exception as e:
        logger.error(f"[EMAIL {timestamp}] FATAL ERROR: {type(e).__name__}: {e}")
        logger.error(f"[EMAIL {timestamp}] Traceback: {traceback.format_exc()}")
        return False


# ============================================================================
# PROFILE VIEWS
# ============================================================================

class UserProfileImageUploadView(APIView):
    """Upload user profile image."""
    
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request):
        """Upload or update profile image (JPG, JPEG, PNG only)."""
        user = request.user
        
        if 'profile_img' not in request.FILES:
            return Response(
                {'profile_img': ['No image file provided.']},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        image = request.FILES['profile_img']
        allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
        
        if image.content_type not in allowed_types:
            return Response(
                {'profile_img': ['Only JPG, JPEG, and PNG files are allowed.']},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
            )
        
        user.profile_img = image
        user.save()
        
        serializer = UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def options(self, request, *args, **kwargs):
        """Handle CORS preflight."""
        response = Response({
            'detail': 'CORS preflight',
            'allowed_methods': ['PUT', 'OPTIONS']
        })
        response['Allow'] = 'PUT, OPTIONS'
        response['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
        response['Access-Control-Allow-Methods'] = 'PUT, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With, X-CSRFToken'
        response['Access-Control-Max-Age'] = '86400'
        return response


class UserProfileView(APIView):
    """Get and update user profile."""
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get current user's profile."""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        """Update current user's profile (full update)."""
        user = request.user
        data = request.data.copy()
        
        serializer = UserDetailSerializer(user, data=data)
        if serializer.is_valid():
            if 'profile_img' in request.FILES:
                user.profile_img = request.FILES['profile_img']
                user.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def options(self, request, *args, **kwargs):
        """Handle CORS preflight."""
        response = Response({
            'detail': 'CORS preflight',
            'allowed_methods': ['GET', 'PUT', 'OPTIONS']
        })
        response['Allow'] = 'GET, PUT, OPTIONS'
        response['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
        response['Access-Control-Allow-Methods'] = 'GET, PUT, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With, X-CSRFToken'
        response['Access-Control-Max-Age'] = '86400'
        return response


class UserProfileUpdateView(APIView):
    """Alias endpoint for profile updates."""
    
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def put(self, request):
        """Update user profile (full update)."""
        user = request.user
        data = request.data.copy()
        
        serializer = UserDetailSerializer(user, data=data)
        if serializer.is_valid():
            if 'profile_img' in request.FILES:
                user.profile_img = request.FILES['profile_img']
                user.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """Partial update user profile."""
        serializer = UserUpdateSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def options(self, request, *args, **kwargs):
        """Handle CORS preflight."""
        response = Response({
            'detail': 'CORS preflight',
            'allowed_methods': ['PUT', 'PATCH', 'OPTIONS']
        })
        response['Allow'] = 'PUT, PATCH, OPTIONS'
        response['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
        response['Access-Control-Allow-Methods'] = 'PUT, PATCH, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With, X-CSRFToken'
        response['Access-Control-Max-Age'] = '86400'
        return response


# ============================================================================
# AUTHENTICATION VIEWSET
# ============================================================================

@method_decorator(csrf_exempt, name='dispatch')
class AuthViewSet(viewsets.ViewSet):
    """Authentication endpoints for user registration, login, verification, etc."""
    
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """
        User registration endpoint.
        POST /api/v1/accounts/auth/register/
        
        Expected payload:
        {
            "email": "user@example.com",
            "password": "securepassword",
            "first_name": "John",
            "last_name": "Doe"
        }
        """
        logger.info('[REGISTER] Registration attempt started')
        logger.info(f'[REGISTER] User: {request.user}, Authenticated: {request.user.is_authenticated}')
        
        serializer = UserRegistrationSerializer(data=request.data)
        
        if not serializer.is_valid():
            logger.warning(f'[REGISTER] Validation failed: {serializer.errors}')
            return Response({
                'success': False,
                'message': 'Registration failed. Please check your input.',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Create user
            user = serializer.save()
            logger.info(f'[REGISTER] User created: {user.email}')
            
            # Generate verification code
            verification_code = generate_verification_code()
            cache_key = f"email_verification_{user.email}"
            cache.set(cache_key, verification_code, timeout=600)  # 10 minutes
            logger.info(f'[REGISTER] Verification code generated for {user.email}: {verification_code}')
            
            # Send verification email (non-blocking)
            email_sent = send_verification_email(user.email, verification_code, 'email_verification')
            logger.info(f'[REGISTER] Email send result: {email_sent}')
            
            # Generate JWT tokens
            try:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                logger.info(f'[REGISTER] Tokens generated successfully for {user.email}')
            except Exception as token_error:
                logger.error(f'[REGISTER] Token generation failed: {token_error}')
                logger.error(f'[REGISTER] Traceback: {traceback.format_exc()}')
                return Response({
                    'success': False,
                    'message': 'Registration successful but token generation failed.',
                    'errors': {'tokens': ['Failed to generate authentication tokens. Please try logging in.']}
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            user_data = UserBasicSerializer(user).data
            
            response_data = {
                'success': True,
                'message': 'Registration successful. Please check your email for verification code.',
                'user': user_data,
                'access': access_token,
                'refresh': refresh_token,
                'email_sent': email_sent,
                'errors': {}
            }
            
            # Add development note if email not sent
            if not email_sent:
                response_data['development_note'] = f'Email not configured. Verification code: {verification_code}'
            
            logger.info(f'[REGISTER] Registration completed successfully for {user.email}')
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f'[REGISTER] Unexpected error: {str(e)}')
            logger.error(f'[REGISTER] Traceback: {traceback.format_exc()}')
            return Response({
                'success': False,
                'message': 'Registration failed due to server error.',
                'errors': {'server': [str(e)]}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """
        User login endpoint.
        POST /api/v1/accounts/auth/login/
        
        Expected payload:
        {
            "email": "user@example.com",
            "password": "password"
        }
        """
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({
                'success': False,
                'message': 'Email and password are required.',
                'errors': {
                    'email': ['Email is required.'] if not email else [],
                    'password': ['Password is required.'] if not password else []
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            logger.warning(f'[LOGIN] User not found: {email}')
            return Response({
                'success': False,
                'message': 'Invalid email or password.',
                'errors': {'credentials': ['Invalid email or password.']}
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.check_password(password):
            logger.warning(f'[LOGIN] Invalid password for user: {email}')
            return Response({
                'success': False,
                'message': 'Invalid email or password.',
                'errors': {'credentials': ['Invalid email or password.']}
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if user is active
        if not user.is_active:
            logger.warning(f'[LOGIN] Inactive user attempted login: {email}')
            return Response({
                'success': False,
                'message': 'Account is not active. Please verify your email.',
                'errors': {'account': ['Account is not active. Please verify your email.']}
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Generate JWT tokens
        try:
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)
            refresh_token = str(refresh)
        except Exception as e:
            logger.error(f'[LOGIN] Token generation failed: {e}')
            return Response({
                'success': False,
                'message': 'Login failed due to token generation error.',
                'errors': {'tokens': ['Failed to generate authentication tokens.']}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        user_data = UserBasicSerializer(user).data
        
        logger.info(f'[LOGIN] User logged in successfully: {email}')
        return Response({
            'success': True,
            'access': access,
            'refresh': refresh_token,
            'user': user_data,
            'message': 'Login successful.'
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def verify_email(self, request):
        """
        Verify email with code.
        POST /api/v1/accounts/auth/verify-email/
        
        Expected payload:
        {
            "email": "user@example.com",
            "code": "123456"
        }
        """
        serializer = EmailVerificationConfirmSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Verification failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        
        # Verify user owns this email
        if str(request.user.email).lower() != str(email).lower():
            return Response({
                'success': False,
                'message': 'Email mismatch.',
                'errors': {'email': ['You can only verify your own email address.']}
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Check verification code
        cache_key = f"email_verification_{email}"
        stored_code = cache.get(cache_key)
        
        if not stored_code:
            logger.warning(f'[VERIFY] No code found for {email}')
            return Response({
                'success': False,
                'message': 'Verification code expired.',
                'resend_prompt': True,
                'errors': {'code': ['Verification code has expired. Please request a new one.']}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if stored_code != code:
            logger.warning(f'[VERIFY] Invalid code for {email}. Expected: {stored_code}, Got: {code}')
            return Response({
                'success': False,
                'message': 'Invalid verification code.',
                'errors': {'code': ['The verification code you entered is incorrect.']}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            user.is_verified = True
            user.is_active = True
            user.save(update_fields=['is_verified', 'is_active', 'date_updated'])
            
            # Clear verification code (single-use)
            cache.delete(cache_key)
            
            # Generate new tokens
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)
            
            logger.info(f'[VERIFY] Email verified successfully for {email}')
            return Response({
                'success': True,
                'message': 'Email verified successfully.',
                'user': UserBasicSerializer(user).data,
                'access': access,
                'refresh': str(refresh),
                'errors': {}
            }, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            logger.error(f'[VERIFY] User not found: {email}')
            return Response({
                'success': False,
                'message': 'User not found.',
                'errors': {'user': ['User not found.']}
            }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='resend-verification')
    def resend_verification(self, request):
        """
        Resend email verification code.
        POST /api/v1/accounts/auth/resend-verification/
        
        Expected payload:
        {
            "email": "user@example.com"
        }
        """
        serializer = EmailVerificationSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Invalid request',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        
        # Rate limiting
        rate_key = f"resend_rate_{email}"
        last_sent = cache.get(rate_key)
        now = int(time.time())
        
        if last_sent and now - last_sent < 60:  # 60 seconds cooldown
            wait_time = 60 - (now - last_sent)
            return Response({
                'success': False,
                'message': f'Please wait {wait_time} seconds before requesting another code.',
                'errors': {'rate_limit': [f'Please wait {wait_time} seconds before requesting another code.']}
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        try:
            user = User.objects.get(email=email)
            
            if user.is_verified:
                return Response({
                    'success': True,
                    'message': 'Email is already verified.',
                    'errors': {}
                }, status=status.HTTP_200_OK)
            
            # Generate new verification code
            verification_code = generate_verification_code()
            cache_key = f"email_verification_{email}"
            cache.set(cache_key, verification_code, timeout=600)  # 10 minutes
            
            logger.info(f'[RESEND] New verification code for {email}: {verification_code}')
            
            # Send verification email
            email_sent = send_verification_email(email, verification_code, 'email_verification')
            
            # Set rate limit
            cache.set(rate_key, now, timeout=60)
            
            response_data = {
                'success': True,
                'message': 'Verification code sent successfully.',
                'email_delivery': 'sent' if email_sent else 'logged',
                'errors': {}
            }
            
            # Add development note if email not sent
            if not email_sent:
                response_data['development_note'] = f'Email not configured. Verification code: {verification_code}'
            
            logger.info(f'[RESEND] Verification code resent for {email}')
            return Response(response_data, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            logger.warning(f'[RESEND] User not found: {email}')
            # Don't reveal if email exists for security
            return Response({
                'success': True,
                'message': 'If the email exists, a verification code has been sent.',
                'errors': {}
            }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def forgot_password(self, request):
        """
        Request password reset code.
        POST /api/v1/accounts/auth/forgot-password/
        
        Expected payload:
        {
            "email": "user@example.com"
        }
        """
        serializer = PasswordResetSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Invalid request',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        
        # Rate limiting
        rate_key = f"password_reset_rate_{email}"
        last_sent = cache.get(rate_key)
        now = int(time.time())
        
        if last_sent and now - last_sent < 60:  # 60 seconds cooldown
            wait_time = 60 - (now - last_sent)
            logger.warning(f'[PASSWORD RESET] Rate limit hit for {email}')
            # Don't reveal rate limiting for security
            return Response({
                'success': True,
                'message': 'If the email exists, a reset code has been sent.'
            }, status=status.HTTP_200_OK)
        
        try:
            user = User.objects.get(email=email)
            
            # Generate and store reset code
            reset_code = generate_verification_code()
            cache_key = f"password_reset_{email}"
            cache.set(cache_key, reset_code, timeout=600)  # 10 minutes
            
            logger.info(f'[PASSWORD RESET] Reset code generated for {email}: {reset_code}')
            
            # Send reset email
            email_sent = send_verification_email(email, reset_code, 'password_reset')
            
            # Set rate limit
            cache.set(rate_key, now, timeout=60)
            
            response_data = {
                'success': True,
                'message': 'Password reset code sent to your email.'
            }
            
            # Add development note if email not sent
            if not email_sent:
                response_data['development_note'] = f'Email not configured. Reset code: {reset_code}'
            
            logger.info(f'[PASSWORD RESET] Reset code sent for {email}')
            return Response(response_data, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            logger.warning(f'[PASSWORD RESET] User not found: {email}')
            # Don't reveal if email exists for security
            return Response({
                'success': True,
                'message': 'If the email exists, a reset code has been sent.'
            }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def reset_password(self, request):
        """
        Reset password with verification code.
        POST /api/v1/accounts/auth/reset-password/
        
        Expected payload:
        {
            "email": "user@example.com",
            "code": "123456",
            "new_password": "newsecurepassword"
        }
        """
        serializer = PasswordResetConfirmSerializer(data=request.data)
        
        if not serializer.is_valid():
            logger.warning(f'[RESET PASSWORD] Validation failed: {serializer.errors}')
            return Response({
                'success': False,
                'message': 'Password reset failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        new_password = serializer.validated_data['new_password']
        
        # Check reset code
        cache_key = f"password_reset_{email}"
        stored_code = cache.get(cache_key)
        
        if not stored_code:
            logger.warning(f'[RESET PASSWORD] No code found for {email}')
            return Response({
                'success': False,
                'message': 'Reset code expired or invalid.',
                'errors': {'code': ['The reset code has expired. Please request a new one.']}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if stored_code != code:
            logger.warning(f'[RESET PASSWORD] Invalid code for {email}')
            return Response({
                'success': False,
                'message': 'Invalid reset code.',
                'errors': {'code': ['The reset code you entered is incorrect.']}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save(update_fields=['password', 'date_updated'])
            
            # Clear reset code (single-use)
            cache.delete(cache_key)
            
            # Clear any rate limits
            cache.delete(f"password_reset_rate_{email}")
            
            logger.info(f'[RESET PASSWORD] Password reset successfully for {email}')
            return Response({
                'success': True,
                'message': 'Password reset successfully. You can now login with your new password.'
            }, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            logger.error(f'[RESET PASSWORD] User not found: {email}')
            return Response({
                'success': False,
                'message': 'User not found.',
                'errors': {'user': ['User not found.']}
            }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def verify_later(self, request):
        """
        Allow user to skip email verification.
        POST /api/v1/accounts/auth/verify-later/
        """
        user = request.user
        user.is_active = True
        user.save(update_fields=['is_active', 'date_updated'])
        
        # Clear any pending verification code
        cache_key = f"email_verification_{user.email}"
        cache.delete(cache_key)
        
        # Generate new tokens
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        
        logger.info(f'[VERIFY LATER] User {user.email} skipped verification')
        return Response({
            'success': True,
            'access': access,
            'refresh': str(refresh),
            'user': UserBasicSerializer(user).data,
            'message': 'Verification skipped. You can verify your email later from your profile.'
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def refresh(self, request):
        """
        Refresh JWT access token using refresh token.
        POST /api/v1/accounts/auth/refresh/
        
        Expected payload:
        {
            "refresh": "refresh_token_here"
        }
        """
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return Response({
                'success': False,
                'error': 'Missing refresh token.',
                'errors': {'refresh': ['Refresh token is required.']}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh_token)
            
            # Get user_id from token payload
            user_id = token.payload.get('user_id')
            if not user_id:
                raise TokenError('Token does not contain user_id')
            
            # Get user object
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise TokenError('User not found')
            
            # Blacklist old token
            try:
                token.blacklist()
            except (AttributeError, TokenError):
                pass  # Blacklist not enabled or already blacklisted
            
            # Generate new tokens
            new_refresh = RefreshToken.for_user(user)
            access_token = str(new_refresh.access_token)
            
            return Response({
                'success': True,
                'access': access_token,
                'refresh': str(new_refresh)
            }, status=status.HTTP_200_OK)
            
        except TokenError as e:
            logger.warning(f'[REFRESH] Invalid token: {e}')
            return Response({
                'success': False,
                'error': 'Invalid or expired refresh token',
                'details': str(e)
            }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.error(f'[REFRESH] Unexpected error: {e}')
            return Response({
                'success': False,
                'error': 'Token refresh failed',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """
        Log out user by blacklisting refresh token.
        POST /api/v1/accounts/auth/logout/
        
        Optional payload:
        {
            "refresh": "refresh_token_here"
        }
        """
        # Capture user email BEFORE clearing session
        user_email = request.user.email if request.user.is_authenticated else 'anonymous'
        logger.info(f'[LOGOUT] User: {user_email}, Authenticated: {request.user.is_authenticated}')
        
        refresh_token = request.data.get('refresh')
        
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                logger.info(f'[LOGOUT] Token blacklisted for {user_email}')
            except TokenError as e:
                logger.warning(f'[LOGOUT] Token blacklist failed: {e}')
                # Don't block logout - still allow user to logout even if token blacklist fails
            except AttributeError:
                logger.warning('[LOGOUT] Token blacklist not enabled')
        else:
            logger.warning(f'[LOGOUT] No refresh token provided by {user_email}')
        
        # Django session logout
        django_logout(request)
        
        # Use captured email (don't access request.user after logout)
        logger.info(f'[LOGOUT] Logout successful for {user_email}')
        return Response({
            'success': True,
            'message': 'Logout successful.'
        }, status=status.HTTP_200_OK)


# ============================================================================
# GOOGLE OAUTH VIEW
# ============================================================================

class GoogleAuthView(APIView):
    """Google OAuth authentication."""
    
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Authenticate with Google access token.
        POST /api/v1/accounts/auth/google/
        
        Expected payload:
        {
            "access_token": "google_access_token_here"
        }
        """
        access_token = request.data.get('access_token')
        
        if not access_token:
            return Response({
                'error': 'Missing access token'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Fetch Google user info
        google_userinfo_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        resp = requests.get(google_userinfo_url, headers=headers)
        
        logger.info(f'[GOOGLE AUTH] Userinfo response: {resp.status_code}')
        
        if resp.status_code != 200:
            logger.error(f'[GOOGLE AUTH] Invalid token: {resp.text}')
            return Response({
                'error': 'Invalid Google access token'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        userinfo = resp.json()

        # Fetch token info to verify audience
        tokeninfo_url = 'https://oauth2.googleapis.com/tokeninfo'
        tokeninfo_resp = requests.get(tokeninfo_url, params={'access_token': access_token})
        
        logger.info(f'[GOOGLE AUTH] Tokeninfo response: {tokeninfo_resp.status_code}')
        
        if tokeninfo_resp.status_code != 200:
            logger.error(f'[GOOGLE AUTH] Token verification failed: {tokeninfo_resp.text}')
            return Response({
                'error': 'Invalid Google token'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        tokeninfo = tokeninfo_resp.json()
        
        expected_aud = str(settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY).strip()
        received_aud = str(tokeninfo.get('aud')).strip()
        
        logger.info(f'[GOOGLE AUTH] Expected aud: {expected_aud}, Received: {received_aud}')
        
        if received_aud != expected_aud:
            logger.error(f'[GOOGLE AUTH] Audience mismatch')
            return Response({
                'error': 'Google token client ID mismatch'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get user details
        email = userinfo.get('email')
        first_name = userinfo.get('given_name', '')
        last_name = userinfo.get('family_name', '')
        picture = userinfo.get('picture', '')

        # Create or get user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'is_active': True,
            }
        )
        
        if created:
            logger.info(f'[GOOGLE AUTH] Created new user: {email}')
        else:
            logger.info(f'[GOOGLE AUTH] Existing user: {email}')
            # Update user details
            if user.first_name != first_name or user.last_name != last_name:
                user.first_name = first_name
                user.last_name = last_name
                user.save(update_fields=['first_name', 'last_name', 'date_updated'])

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        logger.info(f'[GOOGLE AUTH] Login successful for {email}')
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserBasicSerializer(user).data,
            'message': 'Google login successful.'
        }, status=status.HTTP_200_OK)


# ============================================================================
# USER MANAGEMENT VIEWSET
# ============================================================================

class UserViewSet(viewsets.ModelViewSet):
    """User management (admin/developer access only)."""
    
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsDeveloperOrAdmin]

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return UserBasicSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserDetailSerializer

    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Get or update current user profile.
        GET/PATCH /api/v1/accounts/users/me/
        """
        if request.method == 'GET':
            serializer = UserDetailSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif request.method == 'PATCH':
            serializer = UserUpdateSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_balance(self, request):
        """
        Get current user's account balance.
        GET /api/v1/accounts/users/my-balance/
        """
        user = request.user
        return Response({
            'available': float(user.account_balance or 0),
            'pending': 0.0,
            'currency': user.currency or 'USD',
            'last_updated': user.date_updated,
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def add_funds(self, request):
        """
        Add funds to user account.
        POST /api/v1/accounts/users/add-funds/
        
        Expected payload:
        {
            "amount": 100.00,
            "user_id": "optional_for_staff"
        }
        """
        amount = request.data.get('amount')
        target_user = request.user
        
        # Allow staff to credit another user
        user_id = request.data.get('user_id')
        if user_id and request.user.is_staff:
            try:
                target_user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({
                    'detail': 'Target user not found.'
                }, status=status.HTTP_404_NOT_FOUND)

        try:
            amount_dec = Decimal(str(amount))
        except (TypeError, ValueError):
            return Response({
                'detail': 'Invalid amount.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if amount_dec <= 0:
            return Response({
                'detail': 'Amount must be positive.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Update balance
        target_user.account_balance = (target_user.account_balance or Decimal('0')) + amount_dec
        if not target_user.currency:
            target_user.currency = 'USD'
        target_user.save(update_fields=['account_balance', 'currency', 'date_updated'])

        return Response({
            'available': float(target_user.account_balance or 0),
            'pending': 0.0,
            'currency': target_user.currency or 'USD',
            'last_updated': target_user.date_updated,
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def withdraw_funds(self, request):
        """
        Withdraw funds from user account.
        POST /api/v1/accounts/users/withdraw-funds/
        
        Expected payload:
        {
            "amount": 50.00,
            "user_id": "optional_for_staff"
        }
        """
        amount = request.data.get('amount')
        target_user = request.user
        
        user_id = request.data.get('user_id')
        if user_id and request.user.is_staff:
            try:
                target_user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({
                    'detail': 'Target user not found.'
                }, status=status.HTTP_404_NOT_FOUND)

        try:
            amount_dec = Decimal(str(amount))
        except (TypeError, ValueError):
            return Response({
                'detail': 'Invalid amount.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if amount_dec <= 0:
            return Response({
                'detail': 'Amount must be positive.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if (target_user.account_balance or Decimal('0')) < amount_dec:
            return Response({
                'detail': 'Insufficient funds.'
            }, status=status.HTTP_400_BAD_REQUEST)

        target_user.account_balance = (target_user.account_balance or Decimal('0')) - amount_dec
        target_user.save(update_fields=['account_balance', 'date_updated'])

        return Response({
            'available': float(target_user.account_balance or 0),
            'pending': 0.0,
            'currency': target_user.currency or 'USD',
            'last_updated': target_user.date_updated,
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def verify_access(self, request):
        """
        Verify user access for sensitive operations (e.g., accessing payments).
        POST /api/v1/accounts/users/verify_access/
        
        For social login users: Auto-verified (they authenticated with Google/OAuth)
        For password users: Requires password verification
        
        Expected payload:
        {
            "password": "user's password" (only for non-social login users)
        }
        
        Returns:
        {
            "verified": true/false,
            "is_social_login": true/false,
            "message": "Access verified" or error message
        }
        """
        user = request.user
        
        # Social login users (Google, etc.) are auto-verified
        # They already authenticated with a trusted provider
        if user.is_social_login:
            return Response({
                'verified': True,
                'is_social_login': True,
                'message': 'Access verified via social authentication'
            }, status=status.HTTP_200_OK)
        
        # Regular users need password verification
        password = request.data.get('password')
        
        if not password:
            return Response(
                {'verified': False, 'is_social_login': False, 'error': 'Password is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if password is correct
        if user.check_password(password):
            return Response({
                'verified': True,
                'is_social_login': False,
                'message': 'Password verified successfully'
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'verified': False, 'is_social_login': False, 'error': 'Invalid password'},
                status=status.HTTP_401_UNAUTHORIZED
            )

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """
        Change user password.
        POST /api/v1/accounts/users/change-password/
        
        Expected payload:
        {
            "old_password": "currentpassword",
            "new_password": "newsecurepassword"
        }
        """
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save(update_fields=['password', 'date_updated'])
            return Response({
                'message': 'Password changed successfully.'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ============================================================================
# CLIENT PROFILE VIEWSET
# ============================================================================

class ClientProfileViewSet(viewsets.ModelViewSet):
    """Client profile management."""
    
    queryset = ClientProfile.objects.all()
    serializer_class = ClientProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        """Filter queryset based on user role."""
        if self.request.user.role in ['developer', 'admin']:
            return ClientProfile.objects.all()
        elif self.request.user.role == 'client':
            return ClientProfile.objects.filter(user=self.request.user)
        return ClientProfile.objects.none()

    def get_serializer_class(self):
        """Return appropriate serializer."""
        if self.action in ['update', 'partial_update']:
            return ClientProfileUpdateSerializer
        return ClientProfileSerializer


# ============================================================================
# PARTNER VIEWSET
# ============================================================================

class PartnerViewSet(viewsets.ReadOnlyModelViewSet):
    """Public partner listing."""
    
    queryset = Partner.objects.select_related('user').all()
    serializer_class = PartnerPublicSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'head', 'options']
    pagination_class = None

    def get_queryset(self):
        """Filter active partners with search."""
        queryset = super().get_queryset().filter(user__is_active=True)

        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(user__first_name__icontains=search)
                | models.Q(user__last_name__icontains=search)
                | models.Q(professional_title__icontains=search)
                | models.Q(domain__icontains=search)
            )

        queryset = queryset.order_by('-created_at')

        limit = self.request.query_params.get('limit')
        try:
            if limit:
                limit_value = int(limit)
                if limit_value > 0:
                    queryset = queryset[:limit_value]
        except (TypeError, ValueError):
            pass

        return queryset


# ============================================================================
# SECURITY VIEWS
# ============================================================================

class ChangePasswordView(APIView):
    """Change user password (for authenticated users)."""
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Change the user's password."""
        if not request.user.can_change_password:
            return Response({
                'detail': 'Password change is not available for social login users.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Password changed successfully.'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Toggle2FAView(APIView):
    """Toggle 2FA setting."""
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Toggle 2FA for the user."""
        serializer = Toggle2FASerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            user = serializer.save()
            action = "enabled" if user.two_factor_enabled else "disabled"
            
            return Response({
                'success': True,
                'message': f'Two-factor authentication {action} successfully.',
                'data': {
                    'two_factor_enabled': user.two_factor_enabled
                }
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success': False,
            'message': 'Invalid data provided.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        """Get current 2FA status."""
        return Response({
            'two_factor_enabled': request.user.two_factor_enabled
        }, status=status.HTTP_200_OK)