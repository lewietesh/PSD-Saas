# wordknox/middleware.py
import time
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class SessionTimeoutMiddleware(MiddlewareMixin):
    """
    Middleware to handle session timeout after 5 minutes of inactivity
    Only applies to admin panel and authenticated users
    """
    
    def process_request(self, request):
        # Only apply to authenticated users accessing admin panel
        if not request.user.is_authenticated:
            return None
        
        # Skip for API endpoints (JWT handles those)
        if request.path.startswith('/api/'):
            return None
        
        # Get current time
        current_time = time.time()
        
        # Get last activity time from session
        last_activity = request.session.get('last_activity')
        
        if last_activity:
            # Calculate idle time (5 minutes = 300 seconds)
            idle_time = current_time - last_activity
            
            # If idle for more than 5 minutes, logout
            if idle_time > 300:  # 5 minutes
                # Clear all session data
                request.session.flush()
                
                # Logout user
                logout(request)
                
                # Add message for user feedback
                messages.warning(request, 'Your session has expired due to inactivity. Please login again.')
                
                # Redirect to admin login
                if request.path.startswith('/admin/'):
                    return redirect('/admin/login/')
                return redirect('/accounts/login/')
        
        # Update last activity timestamp
        request.session['last_activity'] = current_time
        
        return None
