from django.contrib.auth import authenticate
from django.core.cache import cache
from rest_framework import serializers

from .models import CustomUser, Profile


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        return CustomUser.objects.create_user(email=email, password=password)


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

        if user:
            return user
        raise serializers.ValidationError("Invalid credentials")


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['email', 'first_name', 'last_name', 'gender', 'birthdate', 'image', ]

    def get_email(self, obj):
        return obj.user.email


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class VerifyRestPasswordSerializer(serializers.Serializer):
    otp = serializers.CharField()

    def validate(self, attrs):
        user = self.context['user']
        otp = attrs.get('otp')
        cache_key = f"reset_otp_{user.id}"
        cached_otp = cache.get(cache_key)

        if not cached_otp or cached_otp != otp:
            raise serializers.ValidationError('Invalid OTP.')

        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.is_able_to_reset_password:
            raise serializers.ValidationError('Password reset not allowed.')
        return attrs
