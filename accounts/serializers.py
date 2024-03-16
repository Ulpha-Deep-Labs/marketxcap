# serializers.py
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username_or_email = data.get('username_or_email')
        password = data.get('password')

        # Check if the provided username_or_email is an email
        is_email = '@' in username_or_email

        # Authenticate the user
        user = authenticate(request=self.context.get('request'),
                            username=username_or_email if not is_email else None,
                            email=username_or_email if is_email else None,
                            password=password)

        if not user:
            raise serializers.ValidationError('Invalid login credentials')

        data['user'] = user
        return data
    
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'about', 'avatar']


class CustomUserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'about', 'albums_created', 'images_uploaded', 'subscribed', 'avatar']


class OTPVerificationSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6, min_length=6, write_only=True)
    email= serializers.CharField(max_length=255, min_length=1, write_only=True)


class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class OTPPassVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)  # This field will only be used for write operations