# services/serializers.py
from rest_framework import serializers
from django.utils.text import slugify
from .models import (
    Service, ServiceCategory, ServicePricingTier, ServiceFeature, PricingTierFeature,
    ServiceProcessStep, ServiceDeliverable, ServiceTool, 
    ServicePopularUseCase, ServiceFAQ
)


class ServiceCategorySerializer(serializers.ModelSerializer):
    """
    Basic serializer for service categories
    """
    
    services_count = serializers.SerializerMethodField()
    subcategories_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ServiceCategory
        fields = [
            'id', 'name', 'slug', 'short_desc', 'sub_categories', 'category_url',
            'active', 'sort_order', 'services_count', 'subcategories_count',
            'date_created', 'date_updated'
        ]
        read_only_fields = ['id', 'slug', 'date_created', 'date_updated']
    
    def get_services_count(self, obj):
        """Get count of services in this category"""
        return obj.services.count()
    
    def get_subcategories_count(self, obj):
        """Get count of subcategories"""
        if obj.sub_categories and isinstance(obj.sub_categories, list):
            return len(obj.sub_categories)
        return 0
    
    def validate_name(self, value):
        """Ensure category name is not empty"""
        if not value.strip():
            raise serializers.ValidationError("Category name cannot be empty.")
        return value.strip()
    
    def validate_sub_categories(self, value):
        """Validate subcategories JSON structure"""
        if not value:
            return []
        
        if not isinstance(value, list):
            raise serializers.ValidationError("Subcategories must be a list.")
        
        for i, subcategory in enumerate(value):
            if not isinstance(subcategory, dict):
                raise serializers.ValidationError(f"Subcategory at index {i} must be an object.")
            
            if 'id' not in subcategory or 'name' not in subcategory:
                raise serializers.ValidationError(f"Subcategory at index {i} must have 'id' and 'name' fields.")
            
            if not subcategory['id'].strip() or not subcategory['name'].strip():
                raise serializers.ValidationError(f"Subcategory at index {i} must have non-empty 'id' and 'name' values.")
        
        return value


class ServiceCategoryWithServicesSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for service categories that includes related services
    """
    
    services_count = serializers.SerializerMethodField()
    subcategories_count = serializers.SerializerMethodField()
    services = serializers.SerializerMethodField()
    
    class Meta:
        model = ServiceCategory
        fields = [
            'id', 'name', 'slug', 'short_desc', 'sub_categories', 'category_url',
            'active', 'sort_order', 'services_count', 'subcategories_count',
            'services', 'date_created', 'date_updated'
        ]
        read_only_fields = ['id', 'slug', 'date_created', 'date_updated']
    
    def get_services_count(self, obj):
        """Get count of services in this category"""
        return obj.services.count()
    
    def get_subcategories_count(self, obj):
        """Get count of subcategories"""
        if obj.sub_categories and isinstance(obj.sub_categories, list):
            return len(obj.sub_categories)
        return 0
    
    def get_services(self, obj):
        """Get services in this category"""
        active_services = obj.services.filter(active=True).order_by('sort_order', 'name')
        # Use a simplified service representation to avoid circular imports
        return [
            {
                'id': service.id,
                'name': service.name,
                'slug': service.slug,
                'category': obj.name,  # Use category name from parent
                'description': service.description,
                'pricing_model': service.pricing_model,
                'starting_at': str(service.starting_at) if service.starting_at else None,
                'currency': service.currency,
                'timeline': service.timeline,
                'featured': service.featured,
            }
            for service in active_services
        ]


class ServiceFeatureSerializer(serializers.ModelSerializer):
    """
    Serializer for service features
    """
    
    class Meta:
        model = ServiceFeature
        fields = ['id', 'title', 'description', 'icon_class', 'category', 'included']
        read_only_fields = ['id']

    def validate_title(self, value):
        """Ensure feature title is not empty"""
        if not value.strip():
            raise serializers.ValidationError("Feature title cannot be empty.")
        return value.strip()


class ServicePricingTierSerializer(serializers.ModelSerializer):
    """
    Serializer for service pricing tiers with features
    """
    
    features = serializers.SerializerMethodField()
    
    class Meta:
        model = ServicePricingTier
        fields = [
            'id', 'name', 'price', 'currency', 'unit', 'estimated_delivery',
            'recommended', 'features', 'sort_order'
        ]
        read_only_fields = ['id']
    
    def get_features(self, obj):
        """Get features for this pricing tier"""
        tier_features = PricingTierFeature.objects.filter(
            pricing_tier=obj
        ).select_related('feature')
        
        return [
            {
                'id': tf.feature.id,
                'name': tf.feature.name,
                'description': tf.feature.description,
                'icon_url': tf.feature.icon_url,
                'included': tf.included,
                'sort_order': tf.sort_order
            }
            for tf in tier_features
        ]
    
    def validate_price(self, value):
        """Validate price is non-negative"""
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value


class ServiceProcessStepSerializer(serializers.ModelSerializer):
    """
    Serializer for service process steps
    """
    
    class Meta:
        model = ServiceProcessStep
        fields = ['id', 'title', 'description', 'step_order', 'icon_class']
        read_only_fields = ['id']


class ServiceDeliverableSerializer(serializers.ModelSerializer):
    """
    Serializer for service deliverables
    """
    
    class Meta:
        model = ServiceDeliverable
        fields = ['id', 'description', 'icon_class', 'sort_order']
        read_only_fields = ['id']


class ServiceToolSerializer(serializers.ModelSerializer):
    """
    Serializer for service tools
    """
    
    class Meta:
        model = ServiceTool
        fields = ['id', 'tool_name', 'tool_url', 'icon_url']
        read_only_fields = ['id']


class ServicePopularUsecaseSerializer(serializers.ModelSerializer):
    """
    Serializer for service popular use cases
    """
    
    class Meta:
        model = ServicePopularUseCase
        fields = ['id', 'use_case', 'description']
        read_only_fields = ['id']


class ServiceFAQSerializer(serializers.ModelSerializer):
    """
    Serializer for service FAQs
    """
    
    class Meta:
        model = ServiceFAQ
        fields = ['id', 'question', 'answer', 'sort_order']
        read_only_fields = ['id']
    
    def validate_question(self, value):
        """Ensure question is not empty"""
        if not value.strip():
            raise serializers.ValidationError("Question cannot be empty.")
        return value.strip()
    
    def validate_answer(self, value):
        """Ensure answer is not empty and has minimum length"""
        if not value.strip():
            raise serializers.ValidationError("Answer cannot be empty.")
        if len(value.strip()) < 20:
            raise serializers.ValidationError("Answer must be at least 20 characters long.")
        return value.strip()


class ServiceListSerializer(serializers.ModelSerializer):
    """
    Serializer for service lists
    Includes essential fields and pricing info
    """
    
    category = serializers.SerializerMethodField()
    pricing_tiers_count = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = [
            'id',
            'name',
            'slug',
            'category',
            'description',
            'pricing_model',
            'starting_at',
            'currency',
            'timeline',
            'featured',
            'active',
            'pricing_tiers_count',
            'min_price',
            'date_created'
        ]
    
    def get_category(self, obj):
        """Return category name from service_category relationship"""
        return obj.service_category.name if obj.service_category else None
    
    def get_pricing_tiers_count(self, obj):
        """Return count of pricing tiers"""
        return obj.pricing_tiers.count()
    
    def get_min_price(self, obj):
        """Return minimum price from pricing tiers"""
        min_tier = obj.pricing_tiers.order_by('price').first()
        return min_tier.price if min_tier else obj.starting_at


class ServiceDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for individual services
    Includes all related data and nested relationships
    """
    
    category = serializers.SerializerMethodField()
    service_category = ServiceCategorySerializer(read_only=True)
    pricing_tiers = ServicePricingTierSerializer(many=True, read_only=True)
    process_steps = ServiceProcessStepSerializer(many=True, read_only=True)
    deliverables = ServiceDeliverableSerializer(many=True, read_only=True)
    tools = ServiceToolSerializer(many=True, read_only=True)
    popular_usecases = ServicePopularUsecaseSerializer(many=True, read_only=True)
    faqs = ServiceFAQSerializer(many=True, read_only=True)
    
    class Meta:
        model = Service
        fields = [
            'id',
            'name',
            'slug',
            'service_category',
            'category',
            'description',
            'pricing_model',
            'starting_at',
            'currency',
            'timeline',
            'featured',
            'active',
            'pricing_tiers',
            'process_steps',
            'deliverables',
            'tools',
            'popular_usecases',
            'faqs',
            'date_created',
            'date_updated'
        ]
    
    def get_category(self, obj):
        """Return category name from service_category relationship"""
        return obj.service_category.name if obj.service_category else None


class ServiceCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating services
    Handles nested relationships and business logic
    """
    
    pricing_tiers_data = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        write_only=True,
        help_text="List of pricing tier objects"
    )
    process_steps_data = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        write_only=True,
        help_text="List of process step objects"
    )
    deliverables_data = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        write_only=True,
        help_text="List of deliverable objects"
    )
    tools_data = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        write_only=True,
        help_text="List of tool objects"
    )
    usecases_data = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        write_only=True,
        help_text="List of use case objects"
    )
    faqs_data = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        write_only=True,
        help_text="List of FAQ objects"
    )
    
    # Read-only nested data
    pricing_tiers = ServicePricingTierSerializer(many=True, read_only=True)
    process_steps = ServiceProcessStepSerializer(many=True, read_only=True)
    deliverables = ServiceDeliverableSerializer(many=True, read_only=True)
    tools = ServiceToolSerializer(many=True, read_only=True)
    popular_usecases = ServicePopularUsecaseSerializer(many=True, read_only=True)
    faqs = ServiceFAQSerializer(many=True, read_only=True)
    
    class Meta:
        model = Service
        fields = [
            'id',
            'name',
            'slug',
            'category',
            'description',
            'pricing_model',
            'starting_at',
            'currency',
            'timeline',
            'featured',
            'active',
            'pricing_tiers_data',
            'process_steps_data',
            'deliverables_data',
            'tools_data',
            'usecases_data',
            'faqs_data',
            'pricing_tiers',
            'process_steps',
            'deliverables',
            'tools',
            'popular_usecases',
            'faqs',
            'date_created',
            'date_updated'
        ]
        read_only_fields = ['id', 'date_created', 'date_updated']
    
    def validate_name(self, value):
        """Ensure service name is unique and not empty"""
        if not value.strip():
            raise serializers.ValidationError("Service name cannot be empty.")
        
        # Check for uniqueness (excluding current instance during updates)
        queryset = Service.objects.filter(name__iexact=value.strip())
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise serializers.ValidationError("A service with this name already exists.")
        
        return value.strip()
    
    def validate_description(self, value):
        """Validate description length"""
        if not value.strip():
            raise serializers.ValidationError("Description cannot be empty.")
        if len(value.strip()) < 100:
            raise serializers.ValidationError("Description must be at least 100 characters long.")
        return value.strip()
    
    def validate_starting_at(self, value):
        """Validate starting price is non-negative"""
        if value < 0:
            raise serializers.ValidationError("Starting price cannot be negative.")
        return value
    
    def validate_pricing_tiers_data(self, value):
        """Validate pricing tiers data structure"""
        if not value:
            return value
        
        if len(value) > 5:  # Limit pricing tiers
            raise serializers.ValidationError("Maximum 5 pricing tiers allowed.")
        
        required_fields = ['name', 'price', 'currency']
        
        for i, tier_data in enumerate(value):
            for field in required_fields:
                if field not in tier_data:
                    raise serializers.ValidationError(f"Pricing tier {i+1} must have '{field}' field.")
            
            if tier_data['price'] < 0:
                raise serializers.ValidationError(f"Pricing tier {i+1} price cannot be negative.")
        
        return value
    
    def validate_process_steps_data(self, value):
        """Validate process steps data structure"""
        if not value:
            return value
        
        required_fields = ['title', 'description', 'step_number']
        
        for i, step_data in enumerate(value):
            for field in required_fields:
                if field not in step_data:
                    raise serializers.ValidationError(f"Process step {i+1} must have '{field}' field.")
            
            if not isinstance(step_data['step_number'], int) or step_data['step_number'] <= 0:
                raise serializers.ValidationError(f"Process step {i+1} step_number must be a positive integer.")
        
        return value
    
    def validate(self, data):
        """Cross-field validation"""
        # Auto-generate slug if not provided
        if not data.get('slug') and data.get('name'):
            data['slug'] = slugify(data['name'])
        
        # Validate pricing model and starting_at consistency
        pricing_model = data.get('pricing_model')
        if pricing_model == 'custom' and data.get('starting_at', 0) == 0:
            # For custom pricing, starting_at can be 0
            pass
        elif pricing_model in ['fixed', 'hourly', 'per-page'] and data.get('starting_at', 0) <= 0:
            raise serializers.ValidationError("Starting price must be greater than 0 for this pricing model.")
        
        return data
    
    def create(self, validated_data):
        """Create service with nested relationships"""
        # Extract nested data
        pricing_tiers_data = validated_data.pop('pricing_tiers_data', [])
        process_steps_data = validated_data.pop('process_steps_data', [])
        deliverables_data = validated_data.pop('deliverables_data', [])
        tools_data = validated_data.pop('tools_data', [])
        usecases_data = validated_data.pop('usecases_data', [])
        faqs_data = validated_data.pop('faqs_data', [])
        
        # Handle category field - map to service_category
        category_name = validated_data.pop('category', None)
        if category_name:
            try:
                service_category = ServiceCategory.objects.get(name=category_name)
                validated_data['service_category'] = service_category
            except ServiceCategory.DoesNotExist:
                pass  # Leave service_category as None if category not found
        
        # Create service
        service = Service.objects.create(**validated_data)
        
        # Create pricing tiers
        for tier_data in pricing_tiers_data:
            ServicePricingTier.objects.create(service=service, **tier_data)
        
        # Create process steps
        for step_data in process_steps_data:
            ServiceProcessStep.objects.create(service=service, **step_data)
        
        # Create deliverables
        for deliverable_data in deliverables_data:
            ServiceDeliverable.objects.create(service=service, **deliverable_data)
        
        # Create tools
        for tool_data in tools_data:
            ServiceTool.objects.create(service=service, **tool_data)
        
        # Create use cases
        for usecase_data in usecases_data:
            ServicePopularUseCase.objects.create(service=service, **usecase_data)
        
        # Create FAQs
        for faq_data in faqs_data:
            ServiceFAQ.objects.create(service=service, **faq_data)
        
        return service
    
    def update(self, instance, validated_data):
        """Update service with nested relationships"""
        # Extract nested data
        pricing_tiers_data = validated_data.pop('pricing_tiers_data', None)
        process_steps_data = validated_data.pop('process_steps_data', None)
        deliverables_data = validated_data.pop('deliverables_data', None)
        tools_data = validated_data.pop('tools_data', None)
        usecases_data = validated_data.pop('usecases_data', None)
        faqs_data = validated_data.pop('faqs_data', None)
        
        # Handle category field - map to service_category
        category_name = validated_data.pop('category', None)
        if category_name:
            try:
                service_category = ServiceCategory.objects.get(name=category_name)
                validated_data['service_category'] = service_category
            except ServiceCategory.DoesNotExist:
                validated_data['service_category'] = None
        
        # Update basic fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update pricing tiers if provided
        if pricing_tiers_data is not None:
            instance.pricing_tiers.all().delete()
            for tier_data in pricing_tiers_data:
                ServicePricingTier.objects.create(service=instance, **tier_data)
        
        # Update process steps if provided
        if process_steps_data is not None:
            instance.process_steps.all().delete()
            for step_data in process_steps_data:
                ServiceProcessStep.objects.create(service=instance, **step_data)
        
        # Update deliverables if provided
        if deliverables_data is not None:
            instance.deliverables.all().delete()
            for deliverable_data in deliverables_data:
                ServiceDeliverable.objects.create(service=instance, **deliverable_data)
        
        # Update tools if provided
        if tools_data is not None:
            instance.tools.all().delete()
            for tool_data in tools_data:
                ServiceTool.objects.create(service=instance, **tool_data)
        
        # Update use cases if provided
        if usecases_data is not None:
            instance.popular_usecases.all().delete()
            for usecase_data in usecases_data:
                ServicePopularUseCase.objects.create(service=instance, **usecase_data)
        
        # Update FAQs if provided
        if faqs_data is not None:
            instance.faqs.all().delete()
            for faq_data in faqs_data:
                ServiceFAQ.objects.create(service=instance, **faq_data)
        
        return instance


class PublicServiceListSerializer(serializers.ModelSerializer):
    """
    Public serializer for service lists
    Only shows active services with essential pricing info
    """
    
    min_price = serializers.SerializerMethodField()
    pricing_tiers_count = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = [
            'id',
            'name',
            'slug',
            'category',
            'description',
            'pricing_model',
            'starting_at',
            'currency',
            'timeline',
            'featured',
            'min_price',
            'pricing_tiers_count'
        ]
    
    def get_category(self, obj):
        """Return category name from service_category relationship"""
        return obj.service_category.name if obj.service_category else None
    
    def get_min_price(self, obj):
        """Return minimum price from pricing tiers"""
        min_tier = obj.pricing_tiers.order_by('price').first()
        return min_tier.price if min_tier else obj.starting_at
    
    def get_pricing_tiers_count(self, obj):
        """Return count of pricing tiers"""
        return obj.pricing_tiers.count()


class PublicServiceDetailSerializer(serializers.ModelSerializer):
    """
    Public serializer for individual services
    Full service information for service pages
    """
    
    category = serializers.SerializerMethodField()
    service_category = ServiceCategorySerializer(read_only=True)
    pricing_tiers = ServicePricingTierSerializer(many=True, read_only=True)
    process_steps = ServiceProcessStepSerializer(many=True, read_only=True)
    deliverables = ServiceDeliverableSerializer(many=True, read_only=True)
    tools = ServiceToolSerializer(many=True, read_only=True)
    popular_usecases = ServicePopularUsecaseSerializer(many=True, read_only=True)
    faqs = ServiceFAQSerializer(many=True, read_only=True)
    
    class Meta:
        model = Service
        fields = [
            'id',
            'name',
            'slug',
            'service_category',
            'category',
            'description',
            'pricing_model',
            'starting_at',
            'currency',
            'timeline',
            'featured',
            'pricing_tiers',
            'process_steps',
            'deliverables',
            'tools',
            'popular_usecases',
            'faqs'
        ]
    
    def get_category(self, obj):
        """Return category name from service_category relationship"""
        return obj.service_category.name if obj.service_category else None


class ServiceStatsSerializer(serializers.ModelSerializer):
    """
    Serializer for service statistics (admin use)
    """
    
    category = serializers.SerializerMethodField()
    pricing_tiers_count = serializers.SerializerMethodField()
    process_steps_count = serializers.SerializerMethodField()
    deliverables_count = serializers.SerializerMethodField()
    tools_count = serializers.SerializerMethodField()
    faqs_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = [
            'id',
            'name',
            'category',
            'pricing_model',
            'starting_at',
            'currency',
            'featured',
            'active',
            'pricing_tiers_count',
            'process_steps_count',
            'deliverables_count',
            'tools_count',
            'faqs_count',
            'date_created'
        ]
    
    def get_pricing_tiers_count(self, obj):
        """Count of pricing tiers"""
        return obj.pricing_tiers.count()
    
    def get_process_steps_count(self, obj):
        """Count of process steps"""
        return obj.process_steps.count()
    
    def get_deliverables_count(self, obj):
        """Count of deliverables"""
        return obj.deliverables.count()
    
    def get_tools_count(self, obj):
        """Count of tools"""
        return obj.tools.count()
    
    def get_faqs_count(self, obj):
        """Count of FAQs"""
        return obj.faqs.count()
    
    def get_category(self, obj):
        """Return category name from service_category relationship"""
        return obj.service_category.name if obj.service_category else None