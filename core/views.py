# core/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework import generics

from .models import (
    ContactInfo, NewsletterSubscription, HeroSection, AboutSection,  
    WorkExperience, AboutStats, WhyChooseUs, Roadmap,
    SupportTicket, SupportAttachment, FAQ
)
from .serializers import (
    ContactInfoSerializer, NewsletterSubscriptionSerializer,
    HeroSectionSerializer, HeroSectionListSerializer, PublicHeroSectionSerializer,
    AboutSectionSerializer, AboutSectionListSerializer, PublicAboutSectionSerializer,
    WorkExperienceSerializer, PublicWorkExperienceSerializer,
    AboutStatsSerializer, PublicAboutStatsSerializer,
    WhyChooseUsSerializer, PublicWhyChooseUsSerializer,
    RoadmapSerializer, PublicRoadmapSerializer,
    CompleteAboutDataSerializer,
    SupportTicketSerializer, SupportTicketCreateSerializer, 
    SupportTicketListSerializer, SupportAttachmentSerializer,
    FAQSerializer, PublicFAQSerializer
)

# Newsletter Subscription API View
class NewsletterSubscriptionAPIView(APIView):
    """
    Public API endpoint for newsletter subscriptions
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = NewsletterSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            instance, created = NewsletterSubscription.objects.get_or_create(
                email=serializer.validated_data['email']
            )
            if created:
                return Response({'detail': 'Subscribed successfully.'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail': 'This email is already subscribed.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ViewSet for ContactInfo
class ContactInfoViewSet(viewsets.ModelViewSet):
    queryset = ContactInfo.objects.all()
    serializer_class = ContactInfoSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        # Allow public GET, admin for write
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

# Work Experience ViewSet
class WorkExperienceViewSet(viewsets.ModelViewSet):
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'featured']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return WorkExperience.objects.all()
        return WorkExperience.objects.filter(is_featured=True)
    
    @method_decorator(cache_page(60 * 15))
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured work experiences for public display"""
        featured_experiences = WorkExperience.objects.filter(is_featured=True)
        serializer = PublicWorkExperienceSerializer(featured_experiences, many=True)
        return Response(serializer.data)

# About Stats ViewSet
class AboutStatsViewSet(viewsets.ModelViewSet):
    queryset = AboutStats.objects.all()
    serializer_class = AboutStatsSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'active']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return AboutStats.objects.all()
        return AboutStats.objects.filter(is_active=True)
    
    @method_decorator(cache_page(60 * 15))
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active stats for public display"""
        active_stats = AboutStats.objects.filter(is_active=True)
        serializer = PublicAboutStatsSerializer(active_stats, many=True)
        return Response(serializer.data)

# Why Choose Us ViewSet
class WhyChooseUsViewSet(viewsets.ModelViewSet):
    queryset = WhyChooseUs.objects.all()
    serializer_class = WhyChooseUsSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'active']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return WhyChooseUs.objects.all()
        return WhyChooseUs.objects.filter(is_active=True)
    
    @method_decorator(cache_page(60 * 15))
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active reasons for public display"""
        active_reasons = WhyChooseUs.objects.filter(is_active=True)
        serializer = PublicWhyChooseUsSerializer(active_reasons, many=True)
        return Response(serializer.data)

# Roadmap ViewSet
class RoadmapViewSet(viewsets.ModelViewSet):
    queryset = Roadmap.objects.all()
    serializer_class = RoadmapSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'active']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Roadmap.objects.all()
        return Roadmap.objects.filter(is_active=True)
    
    @method_decorator(cache_page(60 * 15))
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active roadmap items for public display"""
        active_roadmap = Roadmap.objects.filter(is_active=True)
        serializer = PublicRoadmapSerializer(active_roadmap, many=True)
        return Response(serializer.data)

# Hero Section ViewSet
class HeroSectionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing hero sections
    
    - Admin users can CRUD hero sections
    - Public users can only view active hero section
    - Automatically handles "only one active" business rule
    """
    
    queryset = HeroSection.objects.all()
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return HeroSectionListSerializer
        return HeroSectionSerializer
    
    def get_permissions(self):
        """
        Set permissions based on action
        - Public read access for active hero
        - Admin write access for management
        """
        if self.action in ['active_hero', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
    
    def get_queryset(self):
        """Filter queryset based on user permissions"""
        if self.request.user.is_staff:
            return HeroSection.objects.all()
        # Public users only see active hero sections
        return HeroSection.objects.filter(is_active=True)
    
    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    @method_decorator(vary_on_headers('Authorization'))
    @action(detail=False, methods=['get'], url_path='active')
    def active_hero(self, request):
        """
        Get the currently active hero section for public display
        Cached for performance
        """
        try:
            active_hero = HeroSection.objects.get(is_active=True)
            serializer = PublicHeroSectionSerializer(active_hero)
            return Response(serializer.data)
        except HeroSection.DoesNotExist:
            return Response(
                {'detail': 'No active hero section found.'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """
        Activate a specific hero section (deactivates others)
        """
        hero = self.get_object()
        
        with transaction.atomic():
            # Deactivate all other hero sections
            HeroSection.objects.filter(is_active=True).update(is_active=False)
            # Activate this one
            hero.is_active = True
            hero.save()
        
        return Response(
            {'detail': f'Hero section "{hero.heading}" is now active.'}, 
            status=status.HTTP_200_OK
        )
    
    def perform_create(self, serializer):
        """
        Handle creation with business logic
        If new hero is set as active, deactivate others
        """
        instance = serializer.save()
        if instance.is_active:
            with transaction.atomic():
                HeroSection.objects.exclude(pk=instance.pk).update(is_active=False)

# About Section ViewSet
class AboutSectionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing about sections
    
    - Admin users can CRUD about sections
    - Public users can view about content
    """
    
    queryset = AboutSection.objects.all()
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return AboutSectionListSerializer
        return AboutSectionSerializer
    
    def get_permissions(self):
        """
        Set permissions based on action
        - Public read access
        - Admin write access
        """
        if self.action in ['list', 'retrieve', 'latest', 'complete']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
    
    @method_decorator(cache_page(60 * 30))  # Cache for 30 minutes
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """
        Get the latest about section for public display
        Cached for performance
        """
        try:
            latest_about = AboutSection.objects.latest('date_created')
            serializer = PublicAboutSectionSerializer(latest_about)
            return Response(serializer.data)
        except AboutSection.DoesNotExist:
            return Response(
                {'detail': 'No about section found.'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @method_decorator(cache_page(60 * 30))
    @action(detail=False, methods=['get'])
    def complete(self, request):
        """
        Get complete about page data including all related sections
        """
        try:
            about_section = AboutSection.objects.latest('date_created')
            
            data = {
                'about_section': PublicAboutSectionSerializer(about_section).data,
                'work_experience': [],
                'stats': [],
                'why_choose_us': [],
                'roadmap': []
            }
            
            # Only include sections that are enabled
            if about_section.show_work_experience:
                data['work_experience'] = PublicWorkExperienceSerializer(
                    WorkExperience.objects.filter(is_featured=True), many=True
                ).data
            
            if about_section.show_stats:
                data['stats'] = PublicAboutStatsSerializer(
                    AboutStats.objects.filter(is_active=True), many=True
                ).data
            
            if about_section.show_why_choose_us:
                data['why_choose_us'] = PublicWhyChooseUsSerializer(
                    WhyChooseUs.objects.filter(is_active=True), many=True
                ).data
            
            if about_section.show_roadmap:
                data['roadmap'] = PublicRoadmapSerializer(
                    Roadmap.objects.filter(is_active=True), many=True
                ).data
            
            return Response(data)
            
        except AboutSection.DoesNotExist:
            return Response(
                {'detail': 'No about section found.'}, 
                status=status.HTTP_404_NOT_FOUND
            )

# Alternative class-based views for simple cases
class ActiveHeroAPIView(generics.RetrieveAPIView):
    """
    Simple API view to get active hero section
    Alternative to ViewSet action for simpler use cases
    """
    
    serializer_class = PublicHeroSectionSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_object(self):
        # Get page from URL: /api/v1/core/hero/<page>/
        page = self.kwargs.get('page')
        if not page:
            return None
        qs = HeroSection.objects.filter(is_active=True, page=page).order_by('-date_created')
        return qs.first()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response(
                {'detail': 'No active hero section found for this page.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class LatestAboutAPIView(generics.RetrieveAPIView):
    """
    Simple API view to get latest about section
    Alternative to ViewSet action for simpler use cases
    """
    
    serializer_class = PublicAboutSectionSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_object(self):
        try:
            return AboutSection.objects.latest('date_created')
        except AboutSection.DoesNotExist:
            return None
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response(
                {'detail': 'No about section found.'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# Support Ticket Views
class SupportTicketViewSet(viewsets.ModelViewSet):
    """ViewSet for managing support tickets."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter tickets by authenticated user."""
        if self.request.user.is_authenticated:
            if self.request.user.role in ['admin', 'developer']:
                # Admins can see all tickets
                return SupportTicket.objects.select_related('user', 'admin_user').prefetch_related('attachments')
            else:
                # Clients can only see their own tickets
                return SupportTicket.objects.filter(user=self.request.user).select_related('user', 'admin_user').prefetch_related('attachments')
        return SupportTicket.objects.none()
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return SupportTicketCreateSerializer
        elif self.action == 'list':
            return SupportTicketListSerializer
        return SupportTicketSerializer
    
    def perform_create(self, serializer):
        """Set the user when creating a ticket."""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def add_reply(self, request, pk=None):
        """Add admin reply to a support ticket."""
        ticket = self.get_object()
        reply = request.data.get('reply', '').strip()
        
        if not reply:
            return Response(
                {'error': 'Reply cannot be empty'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ticket.admin_reply = reply
        ticket.admin_user = request.user
        ticket.status = 'in_progress'  # Auto-update status when admin replies
        ticket.save()
        
        serializer = self.get_serializer(ticket)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAdminUser])
    def update_status(self, request, pk=None):
        """Update ticket status (admin only)."""
        ticket = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(SupportTicket.STATUS_CHOICES):
            return Response(
                {'error': 'Invalid status'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ticket.status = new_status
        ticket.save()
        
        serializer = self.get_serializer(ticket)
        return Response(serializer.data)


class SupportAttachmentViewSet(viewsets.ModelViewSet):
    """ViewSet for managing support ticket attachments."""
    
    serializer_class = SupportAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter attachments by user's tickets."""
        if self.request.user.role in ['admin', 'developer']:
            return SupportAttachment.objects.all()
        return SupportAttachment.objects.filter(ticket__user=self.request.user)
    
    def perform_create(self, serializer):
        """Validate ticket ownership before creating attachment."""
        ticket_id = self.request.data.get('ticket')
        try:
            ticket = SupportTicket.objects.get(id=ticket_id)
            # Check if user owns the ticket or is admin
            if ticket.user != self.request.user and self.request.user.role not in ['admin', 'developer']:
                raise permissions.PermissionDenied("You can only add attachments to your own tickets.")
            serializer.save(ticket=ticket)
        except SupportTicket.DoesNotExist:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Invalid ticket ID.")


# FAQ ViewSet
class FAQViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing FAQs
    - Public GET access for active FAQs
    - Admin access for all CRUD operations
    """
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    
    def get_permissions(self):
        """Allow public read access, admin for write operations"""
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
    
    def get_queryset(self):
        """Filter FAQs based on user permissions"""
        if self.request.user.is_staff:
            return FAQ.objects.all()
        # Public users only see active FAQs
        return FAQ.objects.filter(is_active=True)
    
    def get_serializer_class(self):
        """Use PublicFAQSerializer for public access"""
        if self.request.user.is_staff:
            return FAQSerializer
        return PublicFAQSerializer
    
    @method_decorator(cache_page(60 * 15))
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured FAQs for public display"""
        featured_faqs = FAQ.objects.filter(is_active=True, featured=True)
        serializer = PublicFAQSerializer(featured_faqs, many=True)
        return Response(serializer.data)
