from django.contrib.auth import authenticate
from django.core.cache import cache
from rest_framework import serializers

from .models import CustomUser, Profile


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class EmailVerificationSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=100)

    def validate(self, data):
        user = self.context['request'].user

        if not user.is_authenticated:
            raise serializers.ValidationError('User is not authenticated')

        cache_key = f"otp_{user.id}"
        cached_otp = cache.get(cache_key)

        if cached_otp is None or cached_otp != data['otp']:
            raise serializers.ValidationError('Invalid or expired OTP')

        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        print(data['email'], data['password'])
        if user:
            return user
        raise serializers.ValidationError("Invalid credentials")


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'gender', 'birthdate', 'image']


class CustomUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = CustomUser
        fields = ['email', 'is_verified', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        self.fields['profile'].update(instance.profile, profile_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
