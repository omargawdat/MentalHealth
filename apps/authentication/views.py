from django.core.cache import cache
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import EmailVerificationSerializer, LoginSerializer, RegisterSerializer
from .utilities.send_otp_email import send_otp_via_email


class UserRegistrationView(APIView):
    permission_classes = []

    @transaction.atomic
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            otp_sent = send_otp_via_email(user.email)
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


from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import CustomUserSerializer


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
