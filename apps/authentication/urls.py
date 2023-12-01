from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import CustomUserDetail, GoogleLogin, LoginView, RegisterView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', CustomUserDetail.as_view(), name='user-detail'),
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
]
