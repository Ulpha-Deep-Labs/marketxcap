# views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import (RegistrationSerializer, LoginSerializer, CustomUserSerializer, CustomUserViewSerializer, 
                          OTPVerificationSerializer, ResendOTPSerializer, PasswordResetSerializer, OTPPassVerificationSerializer)
from rest_framework.authtoken.models import Token
from .email_template import send_welcome_email, send_otp_email
from .models import CustomUser, OTP
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.exceptions import APIException, ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser


class RegistrationAPIView(generics.CreateAPIView):
    """
    Handles user registration through a POST request.
    Upon successful registration, a welcome email is sent to the user.

    Example:
        To register a new user, make a POST request to the 'accounts/register/' endpoint with the required data.

        eg:
        {
            "username": "",
            "email": "",
            "password": ""
        }
    """

    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.perform_create(serializer)

        # Customize the response data
        response_data = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'message': 'User registered successfully'
        }

        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """
        Save the user instance and send a welcome email.
        """
        user = serializer.save()
        send_welcome_email(user.email, user.username)

        # Generate and assign an OTP secret to the user
        otp_token = OTP.generate_otp(user)
        send_otp_email(user.email, otp_token)

        return user
    

class ResendOTPAPIView(generics.CreateAPIView):
    """
    Resends OTP to the user through a POST request.

    Example:
        To resend OTP, make a POST request to the 'accounts/resend-otp/<user_id>/' endpoint with the required data.

        eg:
        {
            "user_id": 1
        }
    """

    serializer_class = ResendOTPSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['email']
        try:
            user = CustomUser.objects.get(email=user_id)
        except ObjectDoesNotExist:
            # If user with the provided email does not exist
            raise ValidationError({'message': 'User with the provided email does not exist'})

        
        user = CustomUser.objects.get(email=user_id)

        # Generate and assign a new OTP secret to the user
        otp_token = OTP.generate_otp(user)
        send_otp_email(user.email, otp_token)

        return Response({'message': 'OTP resent successfully'}, status=status.HTTP_200_OK)



class VerifyEmailAPIView(generics.CreateAPIView):
    """
    Handles email verification through a POST request.

    Example:
        To verify the email, make a POST request to the 'accounts/verify/' endpoint with the required data.

        eg:
        {
            "user_id": 1,  # User ID
            "otp": "123456"  # OTP received in the email
        }
    """

    serializer_class = OTPVerificationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['email']
        try:
            user = CustomUser.objects.get(email=user_id)
        except ObjectDoesNotExist:
            # If user with the provided email does not exist
            raise ValidationError({'message': 'User with the provided email does not exist'}, code='email_error')


        otp_token = serializer.validated_data['otp']

        latest_otp = OTP.objects.filter(user=user).order_by('-created_at').first()

        if latest_otp and latest_otp.is_valid() and latest_otp.code == otp_token:
            user.email_verified = True
            user.save()

            #send_otp_verification_email(user.email, True)

            return Response({'message': 'Email verification successful'}, status=status.HTTP_200_OK)
        else:
            #send_otp_verification_email(user.email, False)

            raise ValidationError({'message': 'Invalid OTP'}, code='otp_error')


class PartialUpdateUserView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class PartialUpdateUserView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    parser_classes = (MultiPartParser, FormParser)
   
    def update(self, request, *args, **kwargs):
        user = self.get_object()

        # Get the serializer with the instance of the current user
        serializer = self.get_serializer(user, data=request.data, partial=True)

        # Validate and save the updated data
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Return a response with the updated data
        return Response(serializer.data)
         



    def get_object(self):
        return self.request.user
    

class UserDetailsView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserViewSerializer

    def get_object(self):
        return self.request.user
        #return self.request.user
    



class PasswordResetAPIView(generics.CreateAPIView):
    """
    Initiates the password reset process through a POST request.

    Example:
        To initiate the password reset, make a POST request to the 'accounts/reset-password/' endpoint with the required data.

        eg:
        {
            "email": "user@example.com"
        }
    """

    serializer_class = PasswordResetSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        try:

            user = get_object_or_404(CustomUser, email=email)
        except:
            raise ValidationError({'message': 'User with the provided email does not exist'}, code='email_error')
        # Generate and assign an OTP secret to the user
        otp_token = OTP.generate_otp(user)

        # Send the OTP to the user's email
        send_otp_email(user.email, otp_token)

        return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
    


class PasswordResetVerifyAPIView(generics.CreateAPIView):
    """
    Verifies the OTP and allows the user to reset the password through a POST request.

    Example:
        To verify the OTP and reset the password, make a POST request to the 'accounts/reset-password/verify/' endpoint with the required data.

        eg:
        {
            "email": "user@example.com",
            "otp": "123456",
            "new_password": "newpassword"
        }
    """

    serializer_class = OTPPassVerificationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp_token = serializer.validated_data['otp']
        new_password = serializer.validated_data['new_password']

        #user = get_object_or_404(CustomUser, email=email)
        try:
            user = get_object_or_404(CustomUser, email=email)
        except Http404:
            # If user with the provided email does not exist
            raise ValidationError({'message': 'User with the provided email does not exist'}, code='email_error')
        
        latest_otp = OTP.objects.filter(user=user).order_by('-created_at').first()

        if latest_otp and latest_otp.is_valid() and latest_otp.code == otp_token:
            # Update user's password
            user.set_password(new_password)
            user.save()

            # Optionally, you can delete the used OTP to prevent reuse
            #latest_otp.delete()

            # Send a password reset success email
            #send_password_reset_email(user.email, True)

            return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
        else:
            # Send a password reset failure email
            #send_password_reset_email(user.email, False)

            raise ValidationError({'message': 'Invalid OTP'})