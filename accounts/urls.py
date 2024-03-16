from django.urls import path, include
from .views import RegistrationAPIView, PartialUpdateUserView, UserDetailsView, VerifyEmailAPIView, ResendOTPAPIView, PasswordResetAPIView, PasswordResetVerifyAPIView

urlpatterns = [
   path('register/', RegistrationAPIView.as_view(), name='registration_api'),
   path('verify-email', VerifyEmailAPIView.as_view(), name='Email_verifcation'),
   path('oauth/', include('drf_social_oauth2.urls', namespace='drf')),
   path('update-user/', PartialUpdateUserView.as_view(), name='partial_update_user'),
   path('user-details/', UserDetailsView.as_view(), name='user_details'),
   path('resend-otp', ResendOTPAPIView.as_view(), name='resend_otp'),
   path('reset-password', PasswordResetAPIView.as_view(), name='password_reset'),
   path('reset-password/verify/', PasswordResetVerifyAPIView.as_view(), name='password_reset_verify'),
    # Add other URLs as needed
]