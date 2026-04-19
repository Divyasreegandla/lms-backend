from django.contrib import admin
from .models import SocialAccount, OTPLog

admin.site.register(SocialAccount)
admin.site.register(OTPLog)