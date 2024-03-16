from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import random
import secrets


from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    subscribed = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    


    def __str__(self):
        return self.username
    
    def subscribe(self):
        self.subscribed = True
        self.save()

class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)

    def is_valid(self):
        # Check if the OTP is still valid (lasts for 10 minutes)
        return timezone.now() - self.created_at < timezone.timedelta(minutes=10)
    
    @classmethod
    def generate_otp(cls, user):
        # Generate a secure random 6-digit OTP
        otp_code = ''.join(secrets.choice("0123456789") for _ in range(6))

        # Create and save the OTP instance
        otp = cls(user=user, code=otp_code)
        otp.save()

        return otp
