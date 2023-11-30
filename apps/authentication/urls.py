from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import CheckUsernameView, CustomUserDetail, LoginView, RegisterUserView, RegisterView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', CustomUserDetail.as_view(), name='user-detail'),
    path('auth/check_usergoogle/', CheckUsernameView.as_view(), name='check_username'),
    path('auth/register_usergoogle/', RegisterUserView.as_view(), name='register_user'),

    # path('auth/google/', GoogleLogin.as_view(), name='google_login'),

]
