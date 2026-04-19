from django.db import models

class SocialAccount(models.Model):
    email = models.EmailField(null=True, blank=True)
    provider = models.CharField(max_length=50)
    provider_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} ({self.provider})"


class OTPLog(models.Model):
    phone = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.phone