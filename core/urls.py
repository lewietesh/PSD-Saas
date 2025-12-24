# core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for ViewSets
router = DefaultRouter()
router.register(r'hero-sections', views.HeroSectionViewSet, basename='herosection')
router.register(r'about-sections', views.AboutSectionViewSet, basename='aboutsection')
router.register(r'contact-info', views.ContactInfoViewSet, basename='contactinfo')
router.register(r'work-experience', views.WorkExperienceViewSet, basename='workexperience')
router.register(r'about-stats', views.AboutStatsViewSet, basename='aboutstats')
router.register(r'why-choose-us', views.WhyChooseUsViewSet, basename='whychooseus')
router.register(r'roadmap', views.RoadmapViewSet, basename='roadmap')
router.register(r'support-tickets', views.SupportTicketViewSet, basename='supportticket')
router.register(r'support-attachments', views.SupportAttachmentViewSet, basename='supportattachment')
router.register(r'faqs', views.FAQViewSet, basename='faq')

# Define URL patterns
urlpatterns = [
    # Include router URLs (provides full CRUD)
    path('', include(router.urls)),
    
    # Alternative simple endpoints (optional - you can choose router or these)
    path('hero/<str:page>/', views.ActiveHeroAPIView.as_view(), name='active-hero'),
    path('about/', views.LatestAboutAPIView.as_view(), name='latest-about'),
    
    # Newsletter subscription endpoint (public)
    path('newsletter/subscribe/', views.NewsletterSubscriptionAPIView.as_view(), name='newsletter-subscribe'),
]

# The router provides these automatic URLs:

# Hero Sections:
# GET    /api/v1/core/hero-sections/          - List all hero sections (admin only)
# POST   /api/v1/core/hero-sections/          - Create hero section (admin only)
# GET    /api/v1/core/hero-sections/{id}/     - Get specific hero section
# PUT    /api/v1/core/hero-sections/{id}/     - Update hero section (admin only)
# PATCH  /api/v1/core/hero-sections/{id}/     - Partial update (admin only)
# DELETE /api/v1/core/hero-sections/{id}/     - Delete hero section (admin only)
# GET    /api/v1/core/hero-sections/active/   - Get active hero (public)
# POST   /api/v1/core/hero-sections/{id}/activate/ - Activate specific hero (admin only)

# About Sections:
# GET    /api/v1/core/about-sections/         - List all about sections (admin only)
# POST   /api/v1/core/about-sections/         - Create about section (admin only)
# GET    /api/v1/core/about-sections/{id}/    - Get specific about section
# PUT    /api/v1/core/about-sections/{id}/    - Update about section (admin only)
# PATCH  /api/v1/core/about-sections/{id}/    - Partial update (admin only)
# DELETE /api/v1/core/about-sections/{id}/    - Delete about section (admin only)
# GET    /api/v1/core/about-sections/latest/  - Get latest about section (public)
# GET    /api/v1/core/about-sections/complete/ - Get complete about page data (public)

# Work Experience:
# GET    /api/v1/core/work-experience/        - List work experiences (public: featured only)
# POST   /api/v1/core/work-experience/        - Create work experience (admin only)
# GET    /api/v1/core/work-experience/{id}/   - Get specific work experience
# PUT    /api/v1/core/work-experience/{id}/   - Update work experience (admin only)
# PATCH  /api/v1/core/work-experience/{id}/   - Partial update (admin only)
# DELETE /api/v1/core/work-experience/{id}/   - Delete work experience (admin only)
# GET    /api/v1/core/work-experience/featured/ - Get featured work experiences (public)

# About Stats:
# GET    /api/v1/core/about-stats/            - List stats (public: active only)
# POST   /api/v1/core/about-stats/            - Create stat (admin only)
# GET    /api/v1/core/about-stats/{id}/       - Get specific stat
# PUT    /api/v1/core/about-stats/{id}/       - Update stat (admin only)
# PATCH  /api/v1/core/about-stats/{id}/       - Partial update (admin only)
# DELETE /api/v1/core/about-stats/{id}/       - Delete stat (admin only)
# GET    /api/v1/core/about-stats/active/     - Get active stats (public)

# Why Choose Us:
# GET    /api/v1/core/why-choose-us/          - List reasons (public: active only)
# POST   /api/v1/core/why-choose-us/          - Create reason (admin only)
# GET    /api/v1/core/why-choose-us/{id}/     - Get specific reason
# PUT    /api/v1/core/why-choose-us/{id}/     - Update reason (admin only)
# PATCH  /api/v1/core/why-choose-us/{id}/     - Partial update (admin only)
# DELETE /api/v1/core/why-choose-us/{id}/     - Delete reason (admin only)
# GET    /api/v1/core/why-choose-us/active/   - Get active reasons (public)

# Roadmap:
# GET    /api/v1/core/roadmap/                - List roadmap items (public: active only)
# POST   /api/v1/core/roadmap/                - Create roadmap item (admin only)
# GET    /api/v1/core/roadmap/{id}/           - Get specific roadmap item
# PUT    /api/v1/core/roadmap/{id}/           - Update roadmap item (admin only)
# PATCH  /api/v1/core/roadmap/{id}/           - Partial update (admin only)
# DELETE /api/v1/core/roadmap/{id}/           - Delete roadmap item (admin only)
# GET    /api/v1/core/roadmap/active/         - Get active roadmap items (public)

# Contact Info:
# GET    /api/v1/core/contact-info/           - List contact info (public)
# POST   /api/v1/core/contact-info/           - Create contact info (admin only)
# GET    /api/v1/core/contact-info/{id}/      - Get specific contact info
# PUT    /api/v1/core/contact-info/{id}/      - Update contact info (admin only)
# PATCH  /api/v1/core/contact-info/{id}/      - Partial update (admin only)
# DELETE /api/v1/core/contact-info/{id}/      - Delete contact info (admin only)

# Simple alternative endpoints:
# GET    /api/v1/core/hero/<page>/            - Get active hero for specific page (public)
# GET    /api/v1/core/about/                  - Get latest about (public)
# POST   /api/v1/core/newsletter/subscribe/   - Subscribe to newsletter (public)