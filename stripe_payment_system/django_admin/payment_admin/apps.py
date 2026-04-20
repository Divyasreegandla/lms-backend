from django.apps import AppConfig

class PaymentAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment_admin'
    verbose_name = 'Payment Management'