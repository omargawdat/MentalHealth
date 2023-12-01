from django.contrib.auth import authenticate
import requests
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import CustomUserSerializer, RegisterSerializer

User = get_user_model()


class GoogleLogin(APIView):
    permission_classes = [AllowAny]

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

            username = google_data['email']  # Using the Google email as username
            user, created = User.objects.get_or_create(username=username)

            if created:
                user.first_name = google_data.get('given_name', '')
                user.last_name = google_data.get('family_name', '')
                user.save()

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'refresh': str(refresh),
                'access': access_token,
            }, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            return Response({'error': 'Failed to retrieve user information'},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            token_data = {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
            return Response({**token_data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({token_type: str(token) for token_type, token in
                             {'access': refresh.access_token, 'refresh': refresh}.items()}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class CustomUserDetail(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
