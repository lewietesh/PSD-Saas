from django.utils import timezone as django_timezone
import pytz
from datetime import datetime
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

User = get_user_model()
# Add this to your google_auth.py to debug timezone issues


class GoogleAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logger = logging.getLogger("google_auth")
        logger.info("=== TIMEZONE DEBUG ===")
        logger.info(f"Django TIME_ZONE setting: {settings.TIME_ZONE}")
        logger.info(f"Django USE_TZ setting: {settings.USE_TZ}")
        logger.info(f"Django timezone.now(): {django_timezone.now()}")
        logger.info(f"System datetime.now(): {datetime.now()}")
        logger.info(f"UTC datetime.now(): {datetime.now(pytz.UTC)}")
        logger.info("=====================")
        
        id_token_str = request.data.get('id_token')
        if not id_token_str:
            return Response({'message': 'Missing id_token'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            import os
            audience = os.environ.get('GOOGLE_CLIENT_ID')
            if not audience:
                return Response({'message': 'Google client ID not configured on server.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Verify the token with Google
            idinfo = id_token.verify_oauth2_token(
                id_token_str,
                google_requests.Request(),
                audience=audience,
                clock_skew_in_seconds=300  # Add 5 minutes tolerance
            )
            
            # Debug token times
            iat = idinfo.get('iat')
            exp = idinfo.get('exp')
            current_utc = int(datetime.now(pytz.UTC).timestamp())
            logger.info(f"[TOKEN DEBUG] iat: {iat}, exp: {exp}, current_utc: {current_utc}")
            logger.info(f"[TOKEN DEBUG] Token valid for: {exp - current_utc} seconds")
            
            email = idinfo.get('email')
            if not email:
                return Response({'message': 'No email in Google token'}, status=status.HTTP_400_BAD_REQUEST)
            
            user, created = User.objects.get_or_create(email=email, defaults={
                'first_name': idinfo.get('given_name', ''),
                'last_name': idinfo.get('family_name', ''),
                'is_active': True,
                'is_verified': True,
                'is_social_login': True,
            })
            
            if created:
                user.set_unusable_password()
                user.save()
            elif not user.is_social_login:
                # Mark existing users who sign in via Google as social login users
                user.is_social_login = True
                user.set_unusable_password()
                user.save(update_fields=['is_social_login'])
            
            # Create JWT token
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            # Debug JWT token times
            jwt_iat = access_token['iat']
            jwt_exp = access_token['exp']
            logger.info(f"[JWT DEBUG] JWT iat: {jwt_iat}, JWT exp: {jwt_exp}")
            logger.info(f"[JWT DEBUG] JWT valid for: {jwt_exp - current_utc} seconds")
            
            return Response({
                'access': str(access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_verified': getattr(user, 'is_verified', True),
                },
                'debug_info': {
                    'django_timezone': str(django_timezone.now()),
                    'utc_now': str(datetime.now(pytz.UTC)),
                    'jwt_expires_in': jwt_exp - current_utc
                }
            })
            
        except ValueError as e:
            error_msg = str(e)
            logger.error(f"[GOOGLE AUTH ERROR] {error_msg}")
            import traceback
            logger.error(traceback.format_exc())
            if 'Token used too early' in error_msg or 'clock' in error_msg:
                return Response({
                    'message': 'Token timing issue detected. Please synchronize your system clock.',
                    'error_type': 'clock_skew',
                    'details': error_msg
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'message': f'Invalid Google token: {error_msg}',
                    'error_type': 'invalid_token'
                }, status=status.HTTP_400_BAD_REQUEST)
