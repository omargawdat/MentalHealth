import requests
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import transaction
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Profile
from .serializers import EmailVerificationSerializer, LoginSerializer, PasswordChangeSerializer, RegisterSerializer, \
    ResetPasswordSerializer, VerifyRestPasswordSerializer
from .serializers import ProfileSerializer
from .utilities.send_otp_email import send_otp_via_email

User = get_user_model()


class UserRegistrationView(APIView):
    permission_classes = []

    @transaction.atomic
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            otp_sent = send_otp_via_email(user.email, "creating an account")
            cache_key = f"otp_{user.id}"
            cache.set(cache_key, str(otp_sent), timeout=300)

            # Generate JWT Tokens
            refresh = RefreshToken.for_user(user)
            return Response(
                {'message': 'User registered. Please check your email for the OTP.',
                 'access': str(refresh.access_token), 'refresh': str(refresh)},
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationView(APIView):

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = EmailVerificationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.is_verified = True
            user.save()
            cache_key = f"otp_{user.id}"
            cache.delete(cache_key)

            return Response(
                {'message': 'Email successfully verified'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendVerificationOtpView(APIView):

    def post(self, request):
        user = request.user
        if user:
            otp_sent = send_otp_via_email(user.email, "resending OTP for account creation")
            cache_key = f"otp_{user.id}"
            cache.set(cache_key, str(otp_sent), timeout=300)
            return Response({'message': 'OTP resent to your email.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)


class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data

            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


class GoogleLogin(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        access_token = request.data.get('token')
        if not access_token:
            return Response({'error': 'Access token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            google_response = requests.get('https://www.googleapis.com/oauth2/v3/userinfo',
                                           params={'access_token': access_token})
            google_data = google_response.json()

            if 'error' in google_data:
                return Response({'error': 'Invalid access token'}, status=status.HTTP_400_BAD_REQUEST)

            user, created = User.objects.get_or_create(email=google_data['email'])
            user.is_verified = True
            user.save()

            if created:
                profile = Profile.objects.create(user=user)
                profile.first_name = google_data.get('given_name', '')
                profile.last_name = google_data.get('family_name', '')
                profile.save()

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            response_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
            return Response({
                'refresh': str(refresh),
                'access': access_token,
            }, status=response_status)

        except requests.exceptions.RequestException as e:
            return Response({'error': 'Failed to retrieve user information'},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendResetOtpView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        otp = send_otp_via_email(user.email, "resetting your password")
        cache_key = f"reset_otp_{user.id}"
        cache.set(cache_key, str(otp), timeout=300)
        return Response({'message': 'OTP sent to your email.'}, status=status.HTTP_200_OK)


class VerifyResetOtpView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = VerifyRestPasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            user = request.user
            user.is_able_to_reset_password = True
            user.save()
            cache_key = f"reset_otp_{user.id}"
            cached_otp = cache.get(cache_key)

            if cached_otp == serializer.validated_data['otp']:
                cache.delete(cache_key)
                return Response({'message': 'OTP verified. You can now reset your password.'},
                                status=status.HTTP_200_OK)

            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.is_able_to_reset_password = False
            user.save()
            return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
