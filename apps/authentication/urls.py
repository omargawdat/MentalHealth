from django.urls import path

from .views import EmailVerificationView, LoginView, UserRegistrationView, UserRetrieveUpdateAPIView

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='login_user'),
    path('auth/register/', UserRegistrationView.as_view(), name='register_user'),
    path('auth/verify-email/', EmailVerificationView.as_view(), name='verify_email'),
    path('auth/user/', UserRetrieveUpdateAPIView.as_view(), name='user-detail'),
]
