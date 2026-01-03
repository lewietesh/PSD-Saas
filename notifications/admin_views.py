# notifications/admin_views.py
"""
Custom admin views for handling message replies
Support replies are now Message records with sender='support' (simplified from MessageReply)
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages as django_messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone

from .models import Message


@staff_member_required
def reply_to_message(request, message_id):
    """
    Custom view to reply to a Message
    Creates a new Message with sender='support' in the same conversation
    """
    message = get_object_or_404(Message, id=message_id)
    
    if request.method == 'POST':
        reply_content = request.POST.get('reply_content', '').strip()
        
        if not reply_content:
            django_messages.error(request, 'Reply content cannot be empty.')
        else:
            # Create support reply as a new Message in the same conversation
            reply = Message.objects.create(
                conversation=message.conversation,
                user=message.user,  # Keep user reference for context
                order=message.order,
                message_type=message.message_type,
                sender='support',
                content=reply_content,
                is_read=False
            )
            
            # Mark original message as read
            if not message.is_read:
                message.is_read = True
                message.save()
            
            django_messages.success(request, 'Reply sent successfully!')
            return redirect('admin:notifications_message_change', message_id)
    
    # Get all messages in this conversation (both user and support)
    conversation_messages = Message.objects.filter(
        conversation=message.conversation
    ).order_by('created_at')
    
    context = {
        'message': message,
        'conversation_messages': conversation_messages,
        'title': f'Reply to Message from {message.user.email if message.user else "User"}',
        'opts': Message._meta,
        'has_view_permission': True,
    }
    
    return render(request, 'admin/notifications/message/reply_form.html', context)


@staff_member_required
@require_http_methods(["POST"])
def quick_reply_api(request):
    """
    AJAX endpoint for quick replies to Messages
    Creates a new Message with sender='support' in the same conversation
    """
    import json
    
    try:
        data = json.loads(request.body)
        message_id = data.get('message_id')
        reply_content = data.get('reply_content', '').strip()
        
        if not reply_content:
            return JsonResponse({'success': False, 'error': 'Reply cannot be empty'}, status=400)
        
        message = get_object_or_404(Message, id=message_id)
        
        # Create support reply as a new Message in the same conversation
        reply = Message.objects.create(
            conversation=message.conversation,
            user=message.user,
            order=message.order,
            message_type=message.message_type,
            sender='support',
            content=reply_content,
            is_read=False
        )
        
        # Mark original message as read
        message.is_read = True
        message.save()
        
        return JsonResponse({
            'success': True,
            'reply_id': str(reply.id),
            'sender': request.user.email,
            'created_at': reply.created_at.strftime('%b %d, %Y %I:%M %p')
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
