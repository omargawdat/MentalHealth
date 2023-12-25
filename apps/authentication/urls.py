from django.urls import path

from .views import CustomUserRetrieveUpdateView, EmailVerificationView, GoogleLogin, LoginView, PasswordChangeView, \
    ResetPasswordView, SendResetOtpView, UserRegistrationView, VerifyResetOtpView

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='login_user'),
    path('auth/register/', UserRegistrationView.as_view(), name='register_user'),
    path('auth/verify-email/', EmailVerificationView.as_view(), name='verify_email'),
    path('auth/user/', CustomUserRetrieveUpdateView.as_view(), name='user-detail'),
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('auth/change-password/', PasswordChangeView.as_view(), name='change-password'),
    path('auth/send-reset-otp/', SendResetOtpView.as_view(), name='send-reset-otp'),
    path('auth/verify-reset-otp/', VerifyResetOtpView.as_view(), name='verify-reset-otp'),
    path('auth/reset-password/', ResetPasswordView.as_view(), name='reset-password'),
]
