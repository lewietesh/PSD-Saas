import django_filters
from .models import Order, Testimonial

class OrderFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(lookup_expr='iexact')
    client = django_filters.CharFilter(field_name='client__id')
    service = django_filters.CharFilter(field_name='service__id')

    class Meta:
        model = Order
        fields = ['status', 'client', 'service', 'date_created']


class TestimonialFilter(django_filters.FilterSet):
    approved = django_filters.BooleanFilter()
    featured = django_filters.BooleanFilter()

    class Meta:
        model = Testimonial
        fields = ['approved', 'featured', 'project', 'service']
