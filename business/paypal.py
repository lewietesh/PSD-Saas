"""
PayPal API utilities for handling PayPal integration
"""
import requests
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, Union

from django.conf import settings
from django.utils import timezone

from django.contrib.auth import get_user_model
from .models import Payment, PayPalPayment, Order
from django.contrib.auth import get_user_model
User = get_user_model()

User = get_user_model()

logger = logging.getLogger(__name__)

class PayPalClient:
    """
    Client for PayPal API operations
    """
    def __init__(self):
        self.client_id = settings.PAYPAL_CLIENT_ID
        self.client_secret = settings.PAYPAL_CLIENT_SECRET
        self.base_url = settings.PAYPAL_API_URL
        self.mode = settings.PAYPAL_MODE
        self.access_token = None
        self.token_expires_at = None
    
    def _get_access_token(self) -> str:
        """
        Get an access token for API requests
        """
        if self.access_token and self.token_expires_at and self.token_expires_at > timezone.now():
            return self.access_token
        
        auth_url = f"{self.base_url}/v1/oauth2/token"
        headers = {
            "Accept": "application/json",
            "Accept-Language": "en_US"
        }
        data = {
            "grant_type": "client_credentials"
        }
        
        try:
            response = requests.post(
                auth_url, 
                auth=(self.client_id, self.client_secret),
                headers=headers,
                data=data
            )
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data['access_token']
            # Calculate expiry time (subtract 5 minutes for safety)
            expires_in_seconds = int(token_data['expires_in']) - 300
            self.token_expires_at = timezone.now() + timezone.timedelta(seconds=expires_in_seconds)
            
            return self.access_token
        except Exception as e:
            logger.error(f"Failed to get PayPal access token: {str(e)}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Response: {e.response.text}")
            raise
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
        """
        Make an authenticated API request to PayPal
        """
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._get_access_token()}"
        }
        
        try:
            if method.lower() == 'get':
                response = requests.get(url, headers=headers, params=params)
            elif method.lower() == 'post':
                response = requests.post(url, headers=headers, data=json.dumps(data) if data else None)
            elif method.lower() == 'patch':
                response = requests.patch(url, headers=headers, data=json.dumps(data) if data else None)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json() if response.content else {}
        
        except Exception as e:
            logger.error(f"PayPal API error: {str(e)}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Response: {e.response.text}")
                try:
                    return e.response.json()
                except:
                    return {"error": str(e), "details": e.response.text if hasattr(e, 'response') else "No response details"}
            raise
    
    def create_order(self, amount: float, currency: str = 'USD', reference_id: str = None, description: str = None) -> Dict:
        """
        Create a PayPal order
        """
        order_data = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": currency,
                        "value": str(amount)
                    },
                    "description": description or "Payment for services"
                }
            ],
            "application_context": {
                "return_url": "https://example.com/return",
                "cancel_url": "https://example.com/cancel"
            }
        }
        
        if reference_id:
            order_data["purchase_units"][0]["reference_id"] = reference_id
        
        return self._make_request('post', 'v2/checkout/orders', order_data)
    
    def capture_order(self, order_id: str) -> Dict:
        """
        Capture an approved PayPal order
        """
        return self._make_request('post', f"v2/checkout/orders/{order_id}/capture")
    
    def get_order_details(self, order_id: str) -> Dict:
        """
        Get details of a PayPal order
        """
        return self._make_request('get', f"v2/checkout/orders/{order_id}")

    def verify_webhook_signature(self, headers: Dict[str, str], body: str) -> bool:
        """
        Verify the authenticity of a PayPal webhook notification
        """
        verification_data = {
            "auth_algo": headers.get('PAYPAL-AUTH-ALGO'),
            "cert_url": headers.get('PAYPAL-CERT-URL'),
            "transmission_id": headers.get('PAYPAL-TRANSMISSION-ID'),
            "transmission_sig": headers.get('PAYPAL-TRANSMISSION-SIG'),
            "transmission_time": headers.get('PAYPAL-TRANSMISSION-TIME'),
            "webhook_id": settings.PAYPAL_WEBHOOK_ID,
            "webhook_event": json.loads(body)
        }
        
        try:
            response = self._make_request('post', 'v1/notifications/verify-webhook-signature', verification_data)
            return response.get('verification_status') == 'SUCCESS'
        except Exception as e:
            logger.error(f"Webhook verification error: {str(e)}")
            return False


def create_paypal_order(order: Order, amount: float) -> Optional[Dict]:
    """
    Create a PayPal order for a system order
    """
    try:
        client = PayPalClient()
        paypal_response = client.create_order(
            amount=amount,
            currency=order.currency or 'USD',
            reference_id=str(order.id),
            description=f"Payment for order {order.id[:8]}"
        )
        
        # Create a pending payment record
        payment = Payment.objects.create(
            order=order,
            amount=amount,
            currency=order.currency or 'USD',
            method='paypal',
            transaction_id=paypal_response.get('id', ''),
            status='pending',
            notes='PayPal payment initiated'
        )
        
        # Save PayPal specific details
        paypal_payment = PayPalPayment.objects.create(
            payment=payment,
            paypal_order_id=paypal_response.get('id', ''),
            paypal_status=paypal_response.get('status', 'CREATED'),
            paypal_intent=paypal_response.get('intent', 'CAPTURE'),
            paypal_create_time=timezone.now(),
            paypal_data=json.dumps(paypal_response)
        )
        
        return {
            'payment_id': payment.id,
            'paypal_order_id': paypal_payment.paypal_order_id,
            'status': paypal_payment.paypal_status,
            'links': paypal_response.get('links', [])
        }
    
    except Exception as e:
        logger.error(f"Error creating PayPal order: {str(e)}")
        return None


def create_paypal_order_for_balance(user, amount: float, description: str = 'Account balance deposit') -> Optional[Dict]:
    """
    Create a PayPal order for a direct account balance deposit
    """
    try:
        client = PayPalClient()
        paypal_response = client.create_order(
            amount=amount,
            currency='USD',  # Default to USD for balance deposits
            reference_id=f"balance-{user.id}",
            description=description
        )
        
        # Create a pending payment record without an order
        payment = Payment.objects.create(
            order=None,  # No order associated with this payment
            user=user,  # Associate directly with user instead
            amount=amount,
            currency='USD',
            method='paypal',
            transaction_id=paypal_response.get('id', ''),
            status='pending',
            notes='PayPal payment for account balance'
        )
        
        # Save PayPal specific details
        paypal_payment = PayPalPayment.objects.create(
            payment=payment,
            paypal_order_id=paypal_response.get('id', ''),
            paypal_status=paypal_response.get('status', 'CREATED'),
            paypal_intent=paypal_response.get('intent', 'CAPTURE'),
            paypal_create_time=timezone.now(),
            paypal_data=json.dumps(paypal_response),
            is_balance_deposit=True  # Flag this as a balance deposit
        )
        
        return {
            'payment_id': payment.id,
            'paypal_order_id': paypal_payment.paypal_order_id,
            'status': paypal_payment.paypal_status,
            'links': paypal_response.get('links', [])
        }
    
    except Exception as e:
        logger.error(f"Failed to create PayPal order: {str(e)}")
        return None


def capture_paypal_payment(paypal_order_id: str, update_balance: bool = False) -> Optional[Dict]:
    """
    Capture an approved PayPal payment
    """
    try:
        # Find the associated payment record
        try:
            paypal_payment = PayPalPayment.objects.get(paypal_order_id=paypal_order_id)
            payment = paypal_payment.payment
        except PayPalPayment.DoesNotExist:
            logger.error(f"No PayPal payment found for order ID: {paypal_order_id}")
            return None
        
        # Capture the payment via PayPal API
        client = PayPalClient()
        capture_response = client.capture_order(paypal_order_id)
        
        if not capture_response:
            logger.error("Failed to capture PayPal payment")
            return {
                'success': False,
                'error': 'Failed to capture payment'
            }
            
        # Update payment status based on capture response
        if capture_response.get('status') == 'COMPLETED':
            payment.status = 'completed'
            payment.save()
            
            # Update the PayPal payment record
            paypal_payment.paypal_status = 'COMPLETED'
            paypal_payment.paypal_update_time = timezone.now()
            
            # Extract payer details if available
            if 'payer' in capture_response:
                paypal_payment.paypal_payer_id = capture_response['payer'].get('payer_id')
                paypal_payment.paypal_payer_email = capture_response['payer'].get('email_address')
            
            # Extract payment ID if available
            if 'purchase_units' in capture_response and capture_response['purchase_units']:
                if 'payments' in capture_response['purchase_units'][0]:
                    captures = capture_response['purchase_units'][0]['payments'].get('captures', [])
                    if captures:
                        paypal_payment.paypal_payment_id = captures[0].get('id')
            
            paypal_payment.paypal_data = json.dumps(capture_response)
            paypal_payment.save()
            
            # Handle different payment types
            updated_user_record = None
            
            # Update account balance if requested or if this is a balance deposit
            if update_balance or paypal_payment.is_balance_deposit:
                user = payment.user or (payment.order.client if payment.order else None)
                if user:
                    # Update user's denormalized account_balance
                    try:
                        user.account_balance = (user.account_balance or 0) + float(payment.amount)
                        if not user.currency:
                            user.currency = payment.currency or 'USD'
                        user.save(update_fields=['account_balance', 'currency', 'date_updated'])
                        updated_user_record = user
                    except Exception as e:
                        logger.error(f"Failed to update user balance: {e}")
            
            # Update order status if this is an order payment
            if payment.order:
                payment.order.payment_status = 'paid'
                payment.order.save()
            
            # Create response with balance info if available
            response = {
                'success': True,
                'payment_id': payment.id,
                'status': 'completed',
                'paypal_details': {
                    'order_id': paypal_payment.paypal_order_id,
                    'status': paypal_payment.paypal_status
                }
            }
            # Include balance info if available
            if updated_user_record:
                response['balance'] = {
                    'currency': updated_user_record.currency or 'USD',
                    'available': float(updated_user_record.account_balance or 0),
                    'pending': 0.0
                }
                
            return response
        
        else:
            logger.warning(f"PayPal payment not completed: {capture_response.get('status')}")
            
            # Update PayPal payment record with current status
            paypal_payment.paypal_status = capture_response.get('status')
            paypal_payment.paypal_update_time = timezone.now()
            paypal_payment.paypal_data = json.dumps(capture_response)
            paypal_payment.save()
            
            return {
                'success': False,
                'payment_id': payment.id,
                'status': payment.status,
                'message': f"Payment not completed: {capture_response.get('status')}"
            }
    
    except Exception as e:
        logger.error(f"Failed to capture PayPal payment: {str(e)}")
        return None


def handle_paypal_webhook(event_type: str, event_data: Dict) -> bool:
    """
    Handle PayPal webhook events
    """
    logger.info(f"Processing PayPal webhook: {event_type}")
    
    try:
        resource = event_data.get('resource', {})
        resource_id = resource.get('id')
        
        if not resource_id:
            logger.warning("No resource ID in webhook payload")
            return False
        
        # Handle payment capture completed
        if event_type == 'PAYMENT.CAPTURE.COMPLETED':
            # Find the related payment record
            order_id = None
            links = resource.get('links', [])
            for link in links:
                if link.get('rel') == 'up':
                    parts = link.get('href', '').split('/')
                    if len(parts) > 0:
                        order_id = parts[-1]
            
            if order_id:
                try:
                    paypal_payment = PayPalPayment.objects.get(paypal_order_id=order_id)
                    payment = paypal_payment.payment
                    
                    # Update payment status
                    payment.status = 'completed'
                    payment.save()
                    
                    # Update PayPal payment details
                    paypal_payment.paypal_payment_id = resource_id
                    paypal_payment.paypal_status = 'COMPLETED'
                    paypal_payment.paypal_update_time = timezone.now()
                    paypal_payment.save()
                    
                    # Update order status if available
                    if payment.order:
                        payment.order.payment_status = 'paid'
                        payment.order.save()
                        
                    # Update account balance if it's a balance deposit
                    if paypal_payment.is_balance_deposit and payment.user:
                        try:
                            u = payment.user
                            u.account_balance = (u.account_balance or 0) + float(payment.amount)
                            if not u.currency:
                                u.currency = payment.currency or 'USD'
                            u.save(update_fields=['account_balance', 'currency', 'date_updated'])
                        except Exception as e:
                            logger.error(f"Failed to update user balance in webhook: {e}")
                    
                    return True
                
                except PayPalPayment.DoesNotExist:
                    logger.error(f"No PayPal payment found for order ID: {order_id}")
                    return False
            
            else:
                logger.warning("Could not determine order ID from webhook payload")
                return False
        
        # Handle payment capture denied or reversed
        elif event_type in ['PAYMENT.CAPTURE.DENIED', 'PAYMENT.CAPTURE.REVERSED']:
            # Logic for failed or reversed payments
            pass
        
        return True
    
    except Exception as e:
        logger.error(f"Failed to process PayPal webhook: {str(e)}")
        return False
