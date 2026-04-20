from django.contrib import admin
from .models import StripePayment

@admin.register(StripePayment)
class StripePaymentAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'user_email', 'amount', 'status', 'payment_type', 'created_at']
    list_filter = ['status', 'payment_type', 'created_at']
    search_fields = ['transaction_id', 'user_email']
    readonly_fields = ['created_at']