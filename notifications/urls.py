# notifications/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'contact-messages', views.ContactMessageViewSet, basename='contactmessage')
router.register(r'general-messages', views.GeneralMessageViewSet, basename='generalmessage')
router.register(r'messages', views.MessageViewSet, basename='message')
router.register(r'anonymous-chat', views.AnonymousChatViewSet, basename='anonymouschat')

urlpatterns = [
    path('', include(router.urls)),
    path('admin-summary/', views.AdminNotificationSummaryView.as_view(), name='admin-notification-summary'),
    path('client-summary/', views.ClientNotificationSummaryView.as_view(), name='client-notification-summary'),
]
