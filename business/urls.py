from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    OrderViewSet,
    ContactMessageViewSet,
    TestimonialViewSet,
    ServiceRequestViewSet,
    PaymentViewSet,
)
from .paypal_views import PayPalViewSet, paypal_webhook


router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'contacts', ContactMessageViewSet, basename='contactmessage')
router.register(r'testimonials', TestimonialViewSet, basename='testimonial')
router.register(r'service-requests', ServiceRequestViewSet, basename='servicerequest')
router.register(r'paypal', PayPalViewSet, basename='paypal')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    path('paypal/webhook/', paypal_webhook, name='paypal_webhook'),
]
