import random
import string

from django.contrib.auth import authenticate, get_user_model
from django.db import transaction
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import CustomUserSerializer, RegisterSerializer

User = get_user_model()


class GoogleLogin(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        token = request.data.get('token')  # Assuming the 'token' is what you're receiving
        redirect_uri = request.data.get('redirect_uri')

        if not token or not redirect_uri:
            return Response({"errors": "Token and redirect_uri must be provided."},
                            status=status.HTTP_400_BAD_REQUEST)

        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=20))

        # Create a random user. In a real scenario, you'd probably have more logic here.
        user = CustomUser.objects.create_user(username=username, password=password)

        # Now, generate JWT token for the new user
        refresh = RefreshToken.for_user(user)
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(response_data, status=status.HTTP_200_OK)


# class GoogleLogin(APIView):
#     def post(self, request, *args, **kwargs):
#         code = request.data.get('code')
#         redirect_uri = request.data.get('redirect_uri')
#
#         if not code or not redirect_uri:
#             return Response({"errors": "Authorization code and redirect_uri must be provided."},
#                             status=status.HTTP_400_BAD_REQUEST)
#
#         strategy = load_strategy(request)
#         backend = load_backend(strategy=strategy, name='google-oauth2', redirect_uri=redirect_uri)
#
#         try:
#             user = backend.auth_complete(code=code)
#         except AuthAlreadyAssociated:
#             return Response({"errors": "This Google account is already associated with another user."},
#                             status=status.HTTP_400_BAD_REQUEST)
#         except AuthException as e:
#             return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#
#         if user and user.is_active:
#             refresh = RefreshToken.for_user(user)
#             response_data = {
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#                 'user': {
#                     'id': user.id,
#                     'username': user.username,
#                     'email': user.email,
#                 }
#             }
#             return Response(response_data, status=status.HTTP_200_OK)
#         else:
#             return Response({"errors": "Authentication failed."}, status=status.HTTP_400_BAD_REQUEST)


# class GoogleLogin(views.APIView):
#     def post(self, request, *args, **kwargs):
#         # Here you expect the token to be passed in the body of the request
#         token = request.data.get('token')
#
#         if not token:
#             return Response({"errors": "No token provided."}, status=status.HTTP_400_BAD_REQUEST)
#
#         # Load the strategy and backend for social-auth
#         strategy = load_strategy(request)
#         backend = load_backend(strategy=strategy, name='google-oauth2', redirect_uri=None)
#
#         # Try to authenticate the user using the token provided
#         try:
#             # In this case, you would be using a method that expects to receive
#             # an 'access_token' directly rather than a redirection from Google with a code.
#             # The backend method needs to be modified to handle the token.
#             user = backend.do_auth(token, strategy=strategy)
#         except AuthAlreadyAssociated:
#             return Response({"errors": "That social media account is already in use."},
#                             status=status.HTTP_400_BAD_REQUEST)
#         except AuthException as e:
#             return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#
#         # If the user is found and active, create a response with the token and user info
#         if user and user.is_active:
#             token = AccessToken.for_user(user)
#             response_data = {
#                 'token': str(token),
#                 'user': {
#                     'id': user.id,
#                     'username': user.username,
#                     'email': user.email,
#                 }
#             }
#             return Response(response_data, status=status.HTTP_200_OK)
#         else:
#             return Response({"errors": "Authentication Failed"}, status=status.HTTP_400_BAD_REQUEST)


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
