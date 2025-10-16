"""
PayPal API Views for handling PayPal integration
"""
import json
import logging
from typing import Dict, Any

from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from .models import Order, Payment, PayPalPayment
from .serializers import PaymentSerializer, PayPalPaymentSerializer
from .paypal import (
    PayPalClient,
    create_paypal_order,
    capture_paypal_payment,
    handle_paypal_webhook,
    create_paypal_order_for_balance,
)

logger = logging.getLogger(__name__)

class PayPalViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   GenericViewSet):
    """
    API endpoints for PayPal integration
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PayPalPaymentSerializer
    
    def get_queryset(self):
        """Filter PayPal payments for current user"""
        user = self.request.user
        if user.is_staff:
            return PayPalPayment.objects.all()
        return PayPalPayment.objects.filter(payment__order__client=user)
    
    @action(detail=False, methods=['post'])
    def create_order(self, request):
        """
        Create a PayPal order and return approval URL
        
        Expected payload:
        {
            "order_id": "order-uuid-here",
            "amount": 100.00
        }
        """
        order_id = request.data.get('order_id')
        amount = request.data.get('amount')
        
        if not order_id:
            return Response(
                {'error': 'Order ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not amount:
            return Response(
                {'error': 'Amount is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Check if this is an account balance deposit or a real order
            description = request.data.get('description', 'Account balance deposit')
            # Support old and new param names
            update_balance = request.data.get('update_balance', request.data.get('update_account_balance', False))
            
            if order_id.startswith('deposit-'):
                # This is a direct balance deposit, not linked to an order
                result = create_paypal_order_for_balance(
                    request.user,
                    float(amount),
                    description
                )
            else:
                # This is a regular order payment
                try:
                    order = Order.objects.get(id=order_id)
                    
                    # Check if user has permission to pay for this order
                    if order.client != request.user and not request.user.is_staff:
                        return Response(
                            {'error': 'You do not have permission to pay for this order'},
                            status=status.HTTP_403_FORBIDDEN
                        )
                    
                    # Create PayPal order
                    result = create_paypal_order(order, float(amount))
                except Order.DoesNotExist:
                    return Response(
                        {'error': 'Order not found'},
                        status=status.HTTP_404_NOT_FOUND
                    )
            
            if not result:
                return Response(
                    {'error': 'Failed to create PayPal order'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Find approval URL
            approval_url = None
            for link in result.get('links', []):
                if link.get('rel') == 'approve':
                    approval_url = link.get('href')
                    break
            
            return Response({
                'paypal_order_id': result.get('paypal_order_id'),
                'status': result.get('status'),
                'approval_url': approval_url,
                'payment_id': result.get('payment_id')
            })
            
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error creating PayPal order: {str(e)}")
            return Response(
                {'error': 'An error occurred creating the PayPal order'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def capture_payment(self, request):
        """
        Capture an approved PayPal payment
        
        Expected payload:
        {
            "paypal_order_id": "paypal-order-id-here"
        }
        """
        paypal_order_id = request.data.get('paypal_order_id')
        
        if not paypal_order_id:
            return Response(
                {'error': 'PayPal order ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Find the PayPal payment
            try:
                paypal_payment = PayPalPayment.objects.get(paypal_order_id=paypal_order_id)
                payment = paypal_payment.payment
                order = payment.order
                
                # Check permissions
                if payment.order:
                    # Regular order payment - check order client permissions
                    if payment.order.client != request.user and not request.user.is_staff:
                        return Response(
                            {'error': 'You do not have permission to capture this payment'},
                            status=status.HTTP_403_FORBIDDEN
                        )
                elif payment.user:
                    # Direct user payment - check user permissions
                    if payment.user != request.user and not request.user.is_staff:
                        return Response(
                            {'error': 'You do not have permission to capture this payment'},
                            status=status.HTTP_403_FORBIDDEN
                        )
                else:
                    # Unknown payment type
                    return Response(
                        {'error': 'Invalid payment record'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
            except PayPalPayment.DoesNotExist:
                return Response(
                    {'error': 'PayPal payment not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Check if we should update account balance
            update_balance = request.data.get('update_balance', request.data.get('update_account_balance', False))
            
            # Capture the payment with balance update if requested
            result = capture_paypal_payment(paypal_order_id, update_balance)
            
            if not result:
                return Response(
                    {'error': 'Failed to capture PayPal payment'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            if result.get('success'):
                response_data = {
                    'success': True,
                    'payment_id': result.get('payment_id'),
                    'status': result.get('status'),
                    'paypal_details': result.get('paypal_details')
                }
                
                # Include account balance if it was updated
                if 'balance' in result:
                    response_data['balance'] = result['balance']
                
                return Response(response_data)
            else:
                return Response({
                    'success': False,
                    'message': result.get('message'),
                    'payment_id': result.get('payment_id'),
                    'status': result.get('status')
                }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Error capturing PayPal payment: {str(e)}")
            return Response(
                {'error': 'An error occurred capturing the PayPal payment'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@method_decorator(csrf_exempt, name='dispatch')
def paypal_webhook(request):
    """
    Handle PayPal webhook notifications
    """
    if request.method != 'POST':
        return HttpResponse(status=405)
    
    try:
        # Get the webhook payload
        payload = json.loads(request.body.decode('utf-8'))
        event_type = payload.get('event_type')
        
        # Verify webhook signature
        client = PayPalClient()
        headers = {
            'PAYPAL-AUTH-ALGO': request.headers.get('PAYPAL-AUTH-ALGO', ''),
            'PAYPAL-CERT-URL': request.headers.get('PAYPAL-CERT-URL', ''),
            'PAYPAL-TRANSMISSION-ID': request.headers.get('PAYPAL-TRANSMISSION-ID', ''),
            'PAYPAL-TRANSMISSION-SIG': request.headers.get('PAYPAL-TRANSMISSION-SIG', ''),
            'PAYPAL-TRANSMISSION-TIME': request.headers.get('PAYPAL-TRANSMISSION-TIME', '')
        }
        
        # Skip verification in sandbox mode for testing
        is_verified = True
        if settings.PAYPAL_MODE == 'live':
            is_verified = client.verify_webhook_signature(headers, request.body.decode('utf-8'))
        
        if not is_verified:
            logger.warning("Invalid PayPal webhook signature")
            return HttpResponse(status=400)
        
        # Process the webhook
        if handle_paypal_webhook(event_type, payload):
            return HttpResponse(status=200)
        else:
            logger.warning(f"Failed to process PayPal webhook: {event_type}")
            return HttpResponse(status=500)
    
    except Exception as e:
        logger.error(f"Error processing PayPal webhook: {str(e)}")
        return HttpResponse(status=500)
