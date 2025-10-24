
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from accounts.admin import BaseAdminPermissions
from .models import ServiceRequest, Order, Testimonial, ContactMessage, Notification, Payment

User = get_user_model()

# Admin for ServiceRequest with file preview/download and conversion to order
@admin.register(ServiceRequest)
class ServiceRequestAdmin(BaseAdminPermissions):
    list_display = (
        'id', 'service', 'pricing_tier', 'name', 'email', 'status', 'created_at', 'attachment_link', 'order_status'
    )
    list_filter = ('status', 'service', 'pricing_tier', 'created_at')
    search_fields = ('id', 'name', 'email', 'project_description', 'budget', 'timeline')
    readonly_fields = ('created_at', 'updated_at', 'attachment_link', 'order_link')
    ordering = ('-created_at',)
    actions = ['convert_to_order', 'mark_as_contacted', 'mark_as_rejected']

    def attachment_link(self, obj):
        if obj.attachment:
            url = obj.attachment.url
            return format_html('<a href="{}" target="_blank">Download</a>', url)
        return "-"
    attachment_link.short_description = "Attachment"

    def order_status(self, obj):
        if obj.order:
            return format_html(
                '<a href="{}" style="color: green;">Order Created</a>',
                reverse('admin:business_order_change', args=[obj.order.id])
            )
        return format_html('<span style="color: orange;">No Order</span>')
    order_status.short_description = "Order Status"

    def order_link(self, obj):
        if obj.order:
            url = reverse('admin:business_order_change', args=[obj.order.id])
            return format_html('<a href="{}">View Order {}</a>', url, str(obj.order.id)[:8])
        return "No order created"
    order_link.short_description = "Related Order"

    def convert_to_order(self, request, queryset):
        """Convert selected service requests to orders"""
        from .utils import convert_service_request_to_order
        
        converted_count = 0
        errors = []
        
        for service_request in queryset:
            order, client_created, error_message = convert_service_request_to_order(service_request)
            
            if error_message:
                errors.append(f"Service request {service_request.id}: {error_message}")
            else:
                converted_count += 1
        
        # Show success/error messages
        if converted_count > 0:
            self.message_user(request, f"Successfully converted {converted_count} service request(s) to order(s).", messages.SUCCESS)
        
        if errors:
            self.message_user(request, f"Errors: {'; '.join(errors)}", messages.ERROR)
    
    convert_to_order.short_description = "Convert selected requests to orders"

    def mark_as_contacted(self, request, queryset):
        """Mark selected service requests as contacted"""
        updated = queryset.update(status='contacted')
        self.message_user(request, f"Marked {updated} service request(s) as contacted.", messages.SUCCESS)
    
    mark_as_contacted.short_description = "Mark as contacted"

    def mark_as_rejected(self, request, queryset):
        """Mark selected service requests as rejected"""
        updated = queryset.update(status='rejected')
        self.message_user(request, f"Marked {updated} service request(s) as rejected.", messages.SUCCESS)
    
    mark_as_rejected.short_description = "Mark as rejected"

@admin.register(Order)
class OrderAdmin(BaseAdminPermissions):
    list_display = ('id', 'client', 'service', 'product', 'status', 'payment_status', 'total_amount', 'attachment_count', 'work_result_count', 'date_created')
    list_filter = ('status', 'payment_status', 'currency', 'date_created')
    search_fields = ('id', 'client__email', 'service__name', 'product__name')
    readonly_fields = ('date_created', 'date_updated', 'attachments_display', 'work_results_display')
    ordering = ('-date_created',)
    actions = ['clear_attachments', 'clear_work_results']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('client', 'service', 'product', 'pricing_tier', 'total_amount', 'currency')
        }),
        ('Status', {
            'fields': ('status', 'payment_status', 'payment_method', 'transaction_id')
        }),
        ('Files', {
            'fields': ('attachments_display', 'work_results_display'),
            'description': 'File attachments and work results associated with this order'
        }),
        ('Additional Information', {
            'fields': ('notes', 'due_date')
        }),
        ('Timestamps', {
            'fields': ('date_created', 'date_updated'),
            'classes': ('collapse',)
        })
    )

    def attachment_count(self, obj):
        """Display count of attachments"""
        count = len(obj.attachments) if obj.attachments else 0
        if count > 0:
            return format_html('<span style="color: green; font-weight: bold;">{}</span>', count)
        return format_html('<span style="color: #ccc;">0</span>')
    attachment_count.short_description = "Attachments"

    def work_result_count(self, obj):
        """Display count of work results"""
        count = len(obj.work_results) if obj.work_results else 0
        if count > 0:
            return format_html('<span style="color: blue; font-weight: bold;">{}</span>', count)
        return format_html('<span style="color: #ccc;">0</span>')
    work_result_count.short_description = "Work Results"

    def attachments_display(self, obj):
        """Display attachment filenames with download links"""
        if not obj.attachments or len(obj.attachments) == 0:
            return format_html('<em style="color: #999;">No attachments</em>')
        
        file_links = []
        for filename in obj.attachments:
            # Construct the media URL for the file
            file_url = f"/media/orders/attachments/{filename}"
            # Extract original filename (remove UUID prefix)
            display_name = filename.split('_', 1)[1] if '_' in filename else filename
            file_links.append(
                format_html(
                    '<div style="margin: 5px 0; padding: 8px; background: #f8f9fa; border-left: 3px solid #28a745; border-radius: 3px;">'
                    '<a href="{}" target="_blank" style="text-decoration: none; color: #155724; font-weight: 500;">'
                    '📎 {}'
                    '</a>'
                    '<small style="display: block; color: #6c757d; margin-top: 2px;">Filename: {}</small>'
                    '</div>',
                    file_url, display_name, filename
                )
            )
        
        return format_html(''.join(file_links))
    attachments_display.short_description = "Client Attachments"

    def work_results_display(self, obj):
        """Display work result filenames with download links"""
        if not obj.work_results or len(obj.work_results) == 0:
            return format_html('<em style="color: #999;">No work results uploaded</em>')
        
        file_links = []
        for filename in obj.work_results:
            # Construct the media URL for the file
            file_url = f"/media/orders/work_results/{filename}"
            # Extract original filename (remove UUID prefix)
            display_name = filename.split('_', 1)[1] if '_' in filename else filename
            file_links.append(
                format_html(
                    '<div style="margin: 5px 0; padding: 8px; background: #f8f9fa; border-left: 3px solid #007bff; border-radius: 3px;">'
                    '<a href="{}" target="_blank" style="text-decoration: none; color: #004085; font-weight: 500;">'
                    '📄 {}'
                    '</a>'
                    '<small style="display: block; color: #6c757d; margin-top: 2px;">Filename: {}</small>'
                    '</div>',
                    file_url, display_name, filename
                )
            )
        
        return format_html(''.join(file_links))
    work_results_display.short_description = "Work Results"

    def clear_attachments(self, request, queryset):
        """Clear all attachments from selected orders"""
        cleared_count = 0
        for order in queryset:
            if order.attachments:
                order.attachments = []
                order.save(update_fields=['attachments'])
                cleared_count += 1
        
        self.message_user(request, f"Cleared attachments from {cleared_count} order(s).", messages.SUCCESS)
    clear_attachments.short_description = "Clear all attachments"

    def clear_work_results(self, request, queryset):
        """Clear all work results from selected orders"""
        cleared_count = 0
        for order in queryset:
            if order.work_results:
                order.work_results = []
                order.save(update_fields=['work_results'])
                cleared_count += 1
        
        self.message_user(request, f"Cleared work results from {cleared_count} order(s).", messages.SUCCESS)
    clear_work_results.short_description = "Clear all work results"


@admin.register(Testimonial)
class TestimonialAdmin(BaseAdminPermissions):
    list_display = ('id', 'client', 'approved', 'featured', 'rating', 'date_created')
    list_filter = ('approved', 'featured', 'rating')
    search_fields = ('client__email', 'content')
    ordering = ('-date_created',)


@admin.register(ContactMessage)
class ContactMessageAdmin(BaseAdminPermissions):
    list_display = ('id', 'name', 'email', 'subject', 'priority', 'source', 'is_read', 'replied', 'date_created')
    list_filter = ('priority', 'source', 'is_read', 'replied', 'date_created')
    search_fields = ('name', 'email', 'subject', 'message')
    ordering = ('-date_created',)


@admin.register(Notification)
class NotificationAdmin(BaseAdminPermissions):
    list_display = ('id', 'user', 'type', 'title', 'priority', 'is_read', 'date_created')
    list_filter = ('type', 'priority', 'is_read')
    search_fields = ('title', 'message', 'user__email')
    ordering = ('-date_created',)


@admin.register(Payment)
class PaymentAdmin(BaseAdminPermissions):
    list_display = ('id', 'order', 'amount', 'currency', 'method', 'status', 'date_created')
    list_filter = ('method', 'status', 'currency')
    search_fields = ('order__id', 'transaction_id', 'order__client__email')
    ordering = ('-date_created',)
